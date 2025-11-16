from playwright.sync_api import sync_playwright, Playwright
import time
import os

# read variables from env, if it isnt set use default values
ORIGIN = os.environ.get("ORIGIN", "Porto Campanha")
DEST = os.environ.get("DEST", "Lisboa Santa Apolonia")
DATE = os.environ.get("DATE", "20/11/2025")


def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    
    print("Going to https://www.cp.pt/pt...")
    page.goto("https://www.cp.pt/pt")
    
    time.sleep(0.5)
    page.locator("#onetrust-accept-btn-handler").click() 
    time.sleep(0.5)

    print(f"Searching for: {ORIGIN} -> {DEST} on {DATE}")

    page.get_by_placeholder("Origem").fill(ORIGIN)
    page.get_by_role("option", name=ORIGIN).click()
    
    time.sleep(0.5)
    
    page.get_by_placeholder("Destino").fill(DEST)
    page.get_by_role("option", name=DEST).click()
    
    time.sleep(0.5)
    
    page.locator("#ida").fill(DATE)
    
    time.sleep(0.5)
    page.click('[aria-label="Pesquisar viagens"]') 
    time.sleep(0.5)
    
    n_trips = page.locator(".departure-time").count()
    print("Number of trips: ", n_trips)
    
    time.sleep(0.5)
    
    for i in range(n_trips):
        print("Departure Time: ", page.locator(".departure-time").nth(i).inner_text()) 
    
    time.sleep(0.5)

    page.screenshot(path="cp_screenshot.png")
    print("Screenshot saved as 'cp_screenshot.png'")
    
    browser.close()

with sync_playwright() as playwright:
    run(playwright)