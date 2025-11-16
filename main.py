from playwright.sync_api import sync_playwright, Playwright
import time
import os
import string
from datetime import datetime

# read variables from env, if it isnt set use default values
ORIGIN = os.environ.get("ORIGIN", "Porto Campanha")
DEST = os.environ.get("DEST", "Lisboa Santa Apolonia")
DATE = os.environ.get("DATE", "20/11/2025")    
LOWER_LIMIT= os.environ.get("LOWER_LIMIT", "08:30") 
UPPER_LIMIT= os.environ.get("UPPER_LIMIT", "17:00") 

# returns True if hour is inside the range of hours
def compare_hours(hour_str, lower_str, upper_str):
    
    # convert time strings into real time objects (!important! assumes the range does not cross midnight)
    hour = datetime.strptime(hour_str, "%H:%M").time()
    lower = datetime.strptime(lower_str, "%H:%M").time()
    upper = datetime.strptime(upper_str, "%H:%M").time()
    
    return lower <= hour <= upper
    
    
def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Going to https://www.cp.pt/pt...")
    page.goto("https://www.cp.pt/pt")
    
    time.sleep(0.8)
    page.locator("#onetrust-accept-btn-handler").click() 
    time.sleep(0.8)

    print(f"Searching for: {ORIGIN} -> {DEST} on {DATE}")

    page.get_by_placeholder("Origem").fill(ORIGIN)
    page.get_by_role("option", name=ORIGIN).click()
    
    time.sleep(0.8)
    
    page.get_by_placeholder("Destino").fill(DEST)
    page.get_by_role("option", name=DEST).click()
    
    time.sleep(0.8)
    
    page.locator("#ida").fill(DATE)
    
    time.sleep(0.8)
    page.click('[aria-label="Pesquisar viagens"]') 
    time.sleep(0.8)
    
    n_trips_by_date = page.locator(".departure-time").count()
    print("Number of trips: ", n_trips_by_date)
    
    time.sleep(0.8)
    
    j = 0
    for i in range(n_trips_by_date):
        departure_time = page.locator(".departure-time").nth(i).inner_text()
        
        if compare_hours(departure_time, LOWER_LIMIT, UPPER_LIMIT) ==  True:
            j += 1
            print(f"Departure Time {j}: {departure_time}")
    
    time.sleep(0.8)
    
    browser.close()

with sync_playwright() as playwright:
    run(playwright)