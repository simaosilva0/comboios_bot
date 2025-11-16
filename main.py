from playwright.sync_api import sync_playwright, Playwright
import time
import os
import string
from datetime import datetime

# read variables from env, if it isnt set use default values
ORIGIN = os.environ.get("ORIGIN", "Espinho")
DEST = os.environ.get("DEST", "Lisboa Santa Apolonia")
DATE = os.environ.get("DATE", "20/11/2025")
LOWER_LIMIT = os.environ.get("LOWER_LIMIT", "08:30")
UPPER_LIMIT = os.environ.get("UPPER_LIMIT", "17:30")
SERVICE = os.environ.get("SERVICE", "Intercidades")

# returns True if hour is inside the range of hours
def compare_hours(hour_str, lower_str, upper_str):

    # convert time strings into real time objects (!important! assumes the range does not cross midnight)
    hour = datetime.strptime(hour_str, "%H:%M").time()
    lower = datetime.strptime(lower_str, "%H:%M").time()
    upper = datetime.strptime(upper_str, "%H:%M").time()

    return lower <= hour <= upper


def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    print("Going to https://www.cp.pt/pt...")
    page.goto("https://www.cp.pt/pt")

    page.locator("#onetrust-accept-btn-handler").click()

    print(f"Searching for: {ORIGIN} -> {DEST} on {DATE}")

    page.get_by_placeholder("Origem").fill(ORIGIN)
    page.get_by_role("option", name=ORIGIN, exact=True).click()

    page.get_by_placeholder("Destino").fill(DEST)
    page.get_by_role("option", name=DEST).click()

    page.locator("#ida").fill(DATE)

    page.click('[aria-label="Pesquisar viagens"]')

    print("Waiting for search results page...")
    page.wait_for_url("**/resultado-pesquisa**")

    page.get_by_label("Filtrar resultados").click()

    page.get_by_role("button", name=SERVICE).click()

    page.get_by_role("button", name="Aplicar filtros").click()

    print("Waiting for filter to apply...")
    page.wait_for_load_state("networkidle")
    
    time.sleep(0.5)

    n_trips_by_date = page.locator(".departure-time").count()
    print(f"Found {n_trips_by_date} trips for {SERVICE}.")

    for i in range(n_trips_by_date):
        departure_time = page.locator(".departure-time").nth(i).inner_text()

        if compare_hours(departure_time, LOWER_LIMIT, UPPER_LIMIT):
            print(f"Found matching time: {departure_time}")

            label_start = f"Selecionar ida das {departure_time}"

            # we use the ^= from CSS to search for text that starts with label_start
            page.locator(f"[aria-label^='{label_start}']").click()

            page.locator(
                "[aria-label='Comprar esta viagem (abre nova janela modal)']"
            ).click()

            page.locator(".custom-checkbox").click()

            page.locator(".confirm-button").click()

            break  # stop after checking the first match
        
    time.sleep(1)    
        
    sold_out_locator = page.get_by_role("button", name="Voltar aos resultados")
    
    if sold_out_locator.is_visible():
        print("No seats available for this train.")
    else:
        # success
        print("Success! Seats are available. Sending notification...")

    print("Scrape complete.")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)