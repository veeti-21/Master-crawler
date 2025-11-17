from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time
import random
import json
import os

import PARAMS


# --- CONFIG ---
OPERA_BINARY = r"C:\Users\Veeti\Downloads\chrome-win64\chrome-win64\chrome.exe"
CHROMEDRIVER_PATH = r"C:\Users\Veeti\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
OUTPUT_FILE = "nettimökki_listings.json"

# --- SETUP SELENIUM ---
options = Options()
options.binary_location = OPERA_BINARY
# options.add_argument("--headless=new")  # run headless if you want
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)  # general wait object

# --- BASE URL ---
BASE_URL = "https://www.nettimokki.com/vuokramokit/"
PARAM = PARAMS.PARAMS




# --- HELPERS ---
def human_pause(a=5.6, b=6.6):
    """Random short pause to mimic human behavior."""
    time.sleep(random.uniform(a, b))

def accept_cookies():
    """
    Quickly dismiss either the standard Nettimökki cookie button or the Alma CMP iframe.
    Loops for a short window so we don't block the crawl waiting for the popup to self-dismiss.
    """
    deadline = time.time() + 12  # give the popup a few seconds to appear
    while time.time() < deadline:
        if _dismiss_alma_cmp_iframe():
            return
        human_pause(0.2, 0.4)

    print("⚠️ Cookie popups not detected within window, continuing without interaction.")
    _cleanup_cookie_overlays()

def _dismiss_alma_cmp_iframe():
    iframe_candidates = driver.find_elements(By.CSS_SELECTOR, "iframe[id^='sp_message_iframe'], iframe[src*='privacy-mgmt']")
    if not iframe_candidates:
        return False

    iframe = iframe_candidates[0]
    try:
        driver.switch_to.frame(iframe)
        cmp_accept = driver.find_element(By.XPATH, "//button[@title='Hyväksy' or normalize-space()='Hyväksy']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cmp_accept)
        human_pause(0.05, 0.2)
        cmp_accept.click()
        print("✅ Dismissed Alma CMP iframe modal.")
        return True
    except NoSuchElementException:
        return False
    except Exception as e:
        print(f"⚠️ Error clicking Alma CMP iframe button: {e}")
        return False
    finally:
        try:
            driver.switch_to.default_content()
        except Exception:
            pass
        _cleanup_cookie_overlays()


def _cleanup_cookie_overlays():
    try:
        driver.execute_script("""
            const modal = document.querySelector('#notice.message.type-modal');
            if (modal) modal.remove();
            document.querySelectorAll('.alma-cmp-overlay, #sp_message_container_1371865, .message.type-modal')
                .forEach(el => el.style.display = 'none');
        """)
    except Exception:
        pass



def scroll_page_slowly():
    """Scroll down gradually like a human to load lazy content."""
    print("Scrolling page like a human...")
    # initial small scrolls to trigger renders
    viewport_height = driver.execute_script("return window.innerHeight")
    scroll_position = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0

    while scroll_position < last_height and attempts < 50:
        step = random.randint(int(viewport_height * 0.25), int(viewport_height * 0.9))
        scroll_position += step
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        human_pause(0.6, 1.4)
        # small jitter scrolls
        if random.random() < 0.4:
            driver.execute_script(f"window.scrollBy(0, {random.randint(-40, 40)});")
            human_pause(0.1, 0.4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > last_height:
            last_height = new_height
        attempts += 1

    # final scroll to bottom to make sure lazy loads start
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    human_pause(1.0, 2.0)
    print("Finished human-like scrolling.")
    # After scrolling, allow some time for dynamic content (like prices) to render
    human_pause(1.2, 2.5)

# --- SCRAPE LIST PAGE ---
def scrape_listing_page(url):
    print(f"\nFetching: {url}")
    driver.get(url)

    # Wait a tiny bit for page core resources (CSS/JS) to start loading
    human_pause(0.6, 1.2)

    # Try to accept cookies if a modal shows up
    accept_cookies()

    # Now scroll like a human to trigger lazy loading
    scroll_page_slowly()

    listings = []

    # Re-locate cards after the page has settled
    try:
        cards = driver.find_elements(By.CSS_SELECTOR, "li.card-list-box")
    except Exception as e:
        print(f"Could not find listing cards: {e}")
        cards = []

    print(f"Found {len(cards)} listings")

    for idx, card in enumerate(cards, start=1):
        try:
            # Use inner find to reduce chance of stale references: find elements fresh for each card
            title_tag = card.find_element(By.CSS_SELECTOR, "div.card-list-title")
            full_html = title_tag.get_attribute("outerHTML")
            print(f"\n[{idx}] --- FULL div.card-list-title HTML ---")
            print(full_html)
            print("--------------------------------------")
            title = title_tag.text.strip() if title_tag else ""

            # location (may not exist for some cards)
            try:
                location_tag = card.find_element(By.CSS_SELECTOR, "div.card-list-location")
                location = location_tag.text.strip()
            except NoSuchElementException:
                location = ""

            # price (may be loaded asynchronously)
            try:
                price_tag = card.find_element(By.CSS_SELECTOR, "div.card-list-calculated-price")
                # sometimes the price is rendered inside child nodes; get text after small pause
                human_pause(0.05, 0.2)
                price = price_tag.text.strip()
            except NoSuchElementException:
                price = ""

            # link
            try:
                link = card.find_element(By.CSS_SELECTOR, "a.content-wrapper").get_attribute("href")
            except NoSuchElementException:
                link = ""

            listings.append({
                "title": title,
                "location": location,
                "price": price,
                "url": link
            })
        except StaleElementReferenceException:
            print(f"Stale element for card #{idx}, skipping.")
        except Exception as e:
            print(f"Error parsing card #{idx}: {e}")

    return listings

# --- SCRAPE DETAIL PAGE ---
def scrape_detail_page(url):
    print(f"Fetching details for: {url}")
    try:
        driver.get(url)
        human_pause(0.8, 1.6)
        # ensure main header and price are present
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        except TimeoutException:
            print("h1 not found on detail page within timeout.")

        title = ""
        location = ""
        price = ""
        try:
            title = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
        except Exception:
            title = ""

        try:
            location_el = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb li:last-child")
            location = location_el[0].text.strip() if location_el else ""
        except Exception:
            location = ""

        try:
            price_el = driver.find_elements(By.CSS_SELECTOR, ".price-tag, .ad-price-value")
            price = price_el[0].text.strip() if price_el else ""
        except Exception:
            price = ""

        return {"title": title, "location": location, "price": price, "url": url}

    except Exception as e:
        print(f"Could not fetch details for {url}: {e}")
        return {"title": "", "location": "", "price": "", "url": url}

# --- MAIN EXECUTION ---

PARAMS.params_clean()
PARAMS.params_set_bedrooms_range(1,3)
PARAMS.params_set_water(True,False,False,True)
PARAMS.params_set_beach(True)
PARAMS.params_set_sauna(False,False,True)
PARAMS.params_set_features(False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,False,False,False,)


print("Starting fresh crawl for listing links...")
new_listings = []
for page in range(1, 2):  # scrape first page(s)
    page_url = PARAMS.get_url(PARAMS.params_clean(PARAM), BASE_URL)              # Nyt hakee parametreillä oikean urlin
    new_listings.extend(scrape_listing_page(page_url))
print(f"Collected {len(new_listings)} listings from pages.")

# --- LOAD EXISTING JSON (if exists) ---
existing_data = {}
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            for row in data:
                existing_data[row["url"]] = row  # use URL as key
        except json.JSONDecodeError:
            print("JSON file empty or invalid, starting fresh.")


# --- MERGE NEW LINKS ---
for item in new_listings:
    if item["url"] not in existing_data:
        existing_data[item["url"]] = item

# --- FILL IN MISSING INFO ---
updated_data = []
for url, row in existing_data.items():
    # if any core fields are missing, fetch detail page
    if not row.get("title") or not row.get("price") or not row.get("location"):
        print(f"Missing info for {url}, fetching details...")
        detail = scrape_detail_page(url)
        updated_data.append(detail)
    else:
        updated_data.append(row)

# --- DROP INCOMPLETE RECORDS BEFORE SAVING ---
complete_data = [
    r for r in updated_data
    if r.get("title") and r.get("location") and r.get("price")
]
removed_count = len(updated_data) - len(complete_data)
if removed_count:
    print(f"Removed {removed_count} listings without full info.")

# --- SAVE FINAL JSON ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(complete_data, f, ensure_ascii=False, indent=2)


print(f"\nDone! Saved {len(complete_data)} complete records to {OUTPUT_FILE}")
driver.quit()