from playwright.sync_api import sync_playwright, Playwright
import time

def run(playwright: Playwright):
    # this will open a browser window, set headless to True for invisibility
    browser = playwright.chromium.launch(headless=False)
    
    page = browser.new_page()
    
    print("Going to https://www.cp.pt/pt...")
    page.goto("https://www.cp.pt/pt")
    
    # wait for page to load
    time.sleep(0.5) # TODO replace with better waits
    
    page.locator("#onetrust-accept-btn-handler").click() # accept cookies button
    
    time.sleep(0.5)
    
    page.get_by_placeholder("Origem").fill("Porto Campanha") # fill origin
    page.get_by_role("option", name="Porto Campanha").click()
    
    time.sleep(0.5)
    
    page.get_by_placeholder("Destino").fill("Lisboa Santa Apolonia") # fill destiny
    page.get_by_role("option", name="Lisboa Santa Apolonia").click()
    
    time.sleep(0.5)
    
    page.locator("#ida").fill("20/11/2025") # fill date
    
    time.sleep(0.5)
    
    page.click('[aria-label="Pesquisar viagens"]') # click search
    
    time.sleep(0.5)

    # Take a screenshot to see what the browser sees
    page.screenshot(path="cp_screenshot.png")
    print("Screenshot saved as 'cp_screenshot.png'")
    
    browser.close()

with sync_playwright() as playwright:
    run(playwright)