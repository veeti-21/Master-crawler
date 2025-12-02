from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
import os
import shutil
import PARAMS



# --- CONFIG ---
OPERA_BINARY = r"C:\Users\veeti\Downloads\chrome-win64\chrome-win64\chrome.exe"
CHROMEDRIVER_PATH = r"C:\Users\veeti\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
OUTPUT_FILE = "nettimökki_listings.json"
OUTPUT_FILE_BACKUP = "nettimökki_listings.json.bak"

RESET_JSON_EACH_RUN = True

# Add a limit for how many listings to scrape after collecting links
MAX_LISTINGS_TO_SCRAPE = 10
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

# Fast cookie handling flag (avoid re-checking after first successful attempt)
COOKIE_HANDLED = False

# --- BASE URL ---
BASE_URL = "https://www.nettimokki.com/vuokramokit/"
PARAM = PARAMS.PARAMS




# --- HELPERS ---
def human_pause(a=5.6, b=6.6):
    """Random short pause to mimic human behavior."""
    time.sleep(random.uniform(a, b))

def accept_cookies():
    global COOKIE_HANDLED
    if COOKIE_HANDLED:
        return

    deadline = time.time() + 12  # give the popup a few seconds to appear
    while time.time() < deadline:
        if _dismiss_alma_cmp_iframe():
            COOKIE_HANDLED = True
            return
        human_pause(0.2, 0.4)

    # If nothing detected within window, mark as handled to avoid repeated checks
    COOKIE_HANDLED = True
    print("Cookie popups not detected within window, continuing without interaction.")
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
        print("Dismissed Alma CMP iframe modal.")
        return True
    except NoSuchElementException:
        return False
    except Exception as e:
        print(f"Error clicking Alma CMP iframe button: {e}")
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





# --- SCRAPE LIST PAGE ---
def get_listing_urls(url):
    """
    Goes to a search result page and quickly scrapes all the listing URLs and main image URLs.
    Returns list of dicts: { "url": "...", "image": "..." }
    """
    print(f"\nFetching listing URLs from: {url}")
    driver.get(url)
    human_pause(0.6, 1.2)
    accept_cookies()  # first call will handle, later calls return immediately

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.card-list-box a.content-wrapper")))
    except TimeoutException:
        print("Could not find listing cards on the page.")
        return []

    link_elements = driver.find_elements(By.CSS_SELECTOR, "li.card-list-box a.content-wrapper")
    results = []
    for el in link_elements:
        href = el.get_attribute("href")
        if not href or "tietopankki" in href.lower():
            continue

        # try to find an img within the card and get its src
        img_src = None
        try:
            img_el = el.find_element(By.CSS_SELECTOR, "img")
            img_src = img_el.get_attribute("src")
        except Exception:
            img_src = None

        results.append({"url": href, "image": img_src})

    print(f"Found {len(results)} listing items (filtered).")
    return results

# --- LOGIC PORTED FROM TEST.PY ---

MONTHS_FI = {
    "tammikuu": 1, "helmikuu": 2, "maaliskuu": 3, "huhtikuu": 4,
    "toukokuu": 5, "kesäkuu": 6, "heinäkuu": 7, "elokuu": 8,
    "syyskuu": 9, "lokakuu": 10, "marraskuu": 11, "joulukuu": 12
}

def find_first_available_range(calendar_id, preferred_lengths=(7, 8)):
    """
    Scans the given datepicker (one month) and finds the first available
    consecutive date span. Accepts 7 or 8 days.
    Works even when the month is split into two <table> elements.
    """

    try:
        # Get all <td> that contain an <a> (bookable and clickable)
        day_cells = driver.find_elements(
            By.XPATH,
            f"//div[@id='{calendar_id}']//td[a and contains(@class, 'bookable-day')]"
        )

        days = []
        for cell in day_cells:
            try:
                # Inner <a> contains the visible day number
                day_num = int(cell.find_element(By.TAG_NAME, "a").text.strip())
                days.append(day_num)
            except:
                continue

        print(f"[DEBUG] Days found in order: {days}")

        # Try each desired length (7 first, then 8)
        for length in preferred_lengths:
            for i in range(len(days)):
                start_day = days[i]
                needed = list(range(start_day, start_day + length))

                # Check if all needed days appear in "days" and in correct order
                if all(d in days for d in needed):
                    # Also confirm the order matches
                    indices = [days.index(d) for d in needed]
                    if indices == list(range(indices[0], indices[0] + length)):
                        end_day = start_day + length - 1
                        print(f"[DEBUG] Found consecutive {length}-day period: {start_day}-{end_day}")
                        return start_day, end_day, length

        print("[DEBUG] No valid 7- or 8-day span found")
        return None

    except Exception as e:
        print(f"[DEBUG] Error scanning range: {e}")
        return None


def find_week_in_month_and_get_price(target_year, target_month_num):
    """
    Navigate to the target month, find a 7- or 8-day available range
    using the FROM calendar, then select the matching TO end date
    and capture the price.

    Returns:
        { "week": "start-end", "days": 7/8, "price": "xxx" }
        or None if no valid span exists.
    """

    try:
        # Wait until datepicker is loaded
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-datepicker-month")))
        human_pause(0.5, 1.0)

        # --- Navigate to the correct month ---
        for _ in range(24):  # safety limit
            year_str = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-year").text.strip()
            month_str = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-month").text.strip()

            current_year = int(year_str)
            current_month_num = MONTHS_FI.get(month_str.lower(), -1)

            if current_year == target_year and current_month_num == target_month_num:
                break

            # If we overshoot → nothing to select
            if current_year > target_year or (current_year == target_year and current_month_num > target_month_num):
                return None

            driver.find_element(By.CSS_SELECTOR, "a.ui-datepicker-next").click()
            time.sleep(0.4)
        else:
            # loop exhausted
            return None

        human_pause(0.3, 0.6)

        # --- FIND FIRST FREE RANGE (7 or 8 days) ---
        found = find_first_available_range("ad_detail_from_datepicker")
        if not found:
            print("  -> No 7/8-day span found in FROM calendar")
            return None

        start_day, end_day, days_needed = found
        print(f"  -> Found free {days_needed}-day span: {start_day}-{end_day}")

        # --- SELECT START DAY ---
        from_xpath = f"//div[@id='ad_detail_from_datepicker']//td[a[text()='{start_day}']]"
        from_btn = wait.until(EC.element_to_be_clickable((By.XPATH, from_xpath)))
        from_btn.click()
        human_pause(0.5, 0.9)

        # --- WAIT FOR TO CALENDAR ---
        wait.until(EC.visibility_of_element_located((By.ID, "ad_detail_to_datepicker")))
        human_pause(0.3, 0.6)

        # --- FIND END DAY IN TO CALENDAR ---
        to_found = find_first_available_range("ad_detail_to_datepicker", preferred_lengths=(days_needed,))
        if not to_found:
            print(f"  -> End date not available in TO calendar (need {days_needed} days)")
            return None

        _, to_end_day, _ = to_found

        # --- SELECT END DAY ---
        to_xpath = f"//div[@id='ad_detail_to_datepicker']//td[a[text()='{to_end_day}']]"
        to_click = wait.until(EC.element_to_be_clickable((By.XPATH, to_xpath)))
        to_click.click()
        human_pause(0.7, 1.3)

        # --- GET PRICE ---
        price_element = wait.until(EC.presence_of_element_located((By.ID, "base_price")))
        if (price_element is None):
            to_xpath = f"//div[@id='ad_detail_to_datepicker']//td[a[text()='{to_end_day+1}']]"
            to_click = wait.until(EC.element_to_be_clickable((By.XPATH, to_xpath)))
            to_click.click()
            human_pause(0.7, 1.3)
            
            price_element = wait.until(EC.presence_of_element_located((By.ID, "base_price")))
        time.sleep(1.0)  # wait for JS computation

        price = price_element.text.strip()
        if not price or "lasketaan" in price.lower():
            print("  -> Price invalid or still loading")
            return None

        print(f"  -> Price OK: {price}")

        return {
            "week": f"{start_day}-{end_day}",
            "days": days_needed,
            "price": price
        }

    except Exception as e:
        print(f"  -> ERROR in find_week_in_month_and_get_price: {e}")
        import traceback
        traceback.print_exc()
        return None


def scrape_details_and_prices(url, months_to_check, year_to_check):
    """
    Scrapes all details for a single listing, including finding available weeks
    and prices for the specified months.
    """
    print(f"\nScraping details for: {url}")
    base_data = {"url": url, "prices_per_month": {}}
    
    try:
        driver.get(url)
        accept_cookies()
        human_pause(0.8, 1.2)

        # --- Scrape static data (title, location) ---
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        base_data["title"] = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
        location_el = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb li:last-child")
        base_data["location"] = location_el[0].text.strip() if location_el else ""
    except Exception as e:
        print(f"  -> Could not scrape base details for {url}: {e}")
        return base_data # Return what we have

    # --- Find prices for each requested month ---
    for month_num in months_to_check:
        print(f"--- Searching for available week in month: {month_num}/{year_to_check} ---")
        price_result = find_week_in_month_and_get_price(year_to_check, month_num)
        base_data["prices_per_month"][month_num] = price_result
        
        # Reload page to reset the calendar state for the next search
        print("  -> Reloading page to reset calendar...")
        driver.get(url)
        human_pause(0.5, 1.0)
    
    return base_data

# --- MAIN EXECUTION ---

# 1. Set parameters and get listing URLs
PARAMS.params_clean()
PARAMS.params_set_bedrooms_range(2,4)
PARAMS.params_set_water(True,False,False,True)
PARAMS.params_set_beach(True)
PARAMS.params_set_sauna(False,False,True)

print("Getting listing URLs from the first page...")
page_url = PARAMS.get_url(PARAMS.params_clean(PARAM), BASE_URL)
listing_urls = get_listing_urls(page_url)

# Limit the number of listings to scrape (e.g., first 10)
if listing_urls:
    original_count = len(listing_urls)
    listing_urls = listing_urls[:MAX_LISTINGS_TO_SCRAPE]
    print(f"Collected {original_count} links, limiting to first {len(listing_urls)} for scraping.")
# 2. Scrape details for each listing
complete_data = []
months_to_check = [6, 8]  # June and August
year_to_check = 2026

for i, item in enumerate(listing_urls):
    print(f"\n--- Processing listing {i+1}/{len(listing_urls)} ---")
    if not item or not item.get("url"):
        continue
    
    url = item.get("url")
    listing_data = scrape_details_and_prices(url, months_to_check, year_to_check)

    # attach image URL discovered on listing card
    listing_data["image"] = item.get("image")
    complete_data.append(listing_data)

# 3. Save results to JSON
if RESET_JSON_EACH_RUN and os.path.exists(OUTPUT_FILE):
    shutil.copy2(OUTPUT_FILE, OUTPUT_FILE_BACKUP)
    print(f"\nBacked up previous JSON to {OUTPUT_FILE_BACKUP}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(complete_data, f, ensure_ascii=False, indent=2)

print(f"\nDone! Saved {len(complete_data)} complete records to {OUTPUT_FILE}")
driver.quit()
