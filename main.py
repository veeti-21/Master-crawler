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
OUTPUT_FILE = r"nettisivu\nettimokki_listings.json"



RESET_JSON_EACH_RUN = True

# Add a limit for how many listings to scrape after collecting links
LISTINGS_TO_SCRAPE = 50
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


def has_none(obj):
    """Return True if obj (dict/list/tree) contains any None value."""
    if isinstance(obj, dict):
        return any(has_none(v) for v in obj.values())
    if isinstance(obj, list):
        return any(has_none(v) for v in obj)
    return obj is None


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

def find_first_available_range(calendar_id, preferred_lengths=(7,8)):

    try:
        bookable_cells = driver.find_elements(
            By.XPATH,
            f"//div[@id='{calendar_id}']//td[a and contains(@class, 'bookable-day')]"
        )

        days = []
        for cell in bookable_cells:
            try:
                day_num = int(cell.find_element(By.TAG_NAME, "a").text.strip())
                days.append(day_num)
            except:
                continue

        days = sorted(days)  # VERY IMPORTANT
        print(f"[DEBUG] Bookable days: {days}")

        for length in preferred_lengths:
            for i in range(len(days)):
                start = days[i]
                end = start + length - 1
                needed = list(range(start, end + 1))

                # Check if all needed days exist
                if all(d in days for d in needed):
                    return start, end, length

        return None

    except Exception as e:
        print(f"Range scan error: {e}")
        return None



def find_week_in_month_and_get_price(target_year, target_month_num):
    """
    Navigate to the target month, find a 7- or 8-day available range
    using the FROM calendar, then select the matching TO end date
    and capture the price.
    """

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-datepicker-month")))
        human_pause(0.5, 1.0)

        # --- Navigate to the month ---
        for _ in range(24):
            year_str = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-year").text.strip()
            month_str = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-month").text.strip()

            current_year = int(year_str)
            current_month_num = MONTHS_FI.get(month_str.lower(), -1)

            if current_year == target_year and current_month_num == target_month_num:
                break

            if current_year > target_year or (current_year == target_year and current_month_num > target_month_num):
                return None

            driver.find_element(By.CSS_SELECTOR, "a.ui-datepicker-next").click()
            time.sleep(0.4)
        else:
            return None

        human_pause(0.3, 0.6)

        # --- FIND A 7/8 DAY RANGE IN FROM CALENDAR ---
        found = find_first_available_range("ad_detail_from_datepicker")
        if not found:
            print("  -> No 7/8-day span found")
            return None

        start_day, end_day, days_needed = found
        print(f"  -> Span found: {start_day}-{end_day} ({days_needed} days)")

        # --- SELECT START DAY ---
        from_xpath = f"//div[@id='ad_detail_from_datepicker']//td[a[text()='{start_day}']]"
        from_btn = wait.until(EC.element_to_be_clickable((By.XPATH, from_xpath)))
        from_btn.click()
        human_pause(0.5, 0.9)

        # --- OPEN TO CALENDAR ---
        wait.until(EC.visibility_of_element_located((By.ID, "ad_detail_to_datepicker")))
        human_pause(0.3, 0.6)

        # --- CLICK END DAY (no scanning, no to_end_day) ---
        to_xpath = f"//div[@id='ad_detail_to_datepicker']//td[a[text()='{end_day}']]"

                # --- CLICK END DAY (fallback to next day if needed) ---
        def try_click(day):
            xpath = f"//div[@id='ad_detail_to_datepicker']//td[a[text()='{day}']]"
            try:
                elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                elem.click()
                return True
            except:
                return False

        print(f"  -> Attempting to click end day {end_day}")

        # Try main end_day
        if not try_click(end_day):

            print(f"  -> End day {end_day} failed, trying fallback {end_day + 1}")

            # Try fallback one day forward
            fallback_day = end_day + 1
            if not try_click(fallback_day):
                print(f"  -> Fallback day {fallback_day} also failed")
                return None
            
            # If fallback worked, update end_day and days_needed
            end_day = fallback_day
            days_needed += 1

        human_pause(0.7, 1.3)


        # --- GET PRICE ---
        price_element = wait.until(EC.presence_of_element_located((By.ID, "base_price")))
        time.sleep(1.0)

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

# 1. Set parameters
PARAMS.params_clean()
PARAMS.params_set_bedrooms_range(2,4)
PARAMS.params_set_water(True,False,False,True)
PARAMS.params_set_beach(True)
PARAMS.params_set_sauna(False,False,True)

# How many valid listings we want
TARGET_VALID_LISTINGS = LISTINGS_TO_SCRAPE
MAX_PAGES = 30  # safety cap to avoid infinite pagination

print(f"Collecting up to {TARGET_VALID_LISTINGS} valid listings (skips with missing data will trigger paging)...")

# base search page URL (page 1)
base_page_url = PARAMS.get_url(PARAMS.params_clean(PARAM), BASE_URL)

months_to_check = [7, 8]
year_to_check = 2026

valid_listings = []
seen_urls = set()
page_num = 1

while len(valid_listings) < TARGET_VALID_LISTINGS and page_num <= MAX_PAGES:
    # construct page URL (page 1 = base, subsequent pages add &page=N)
    page_url = base_page_url if page_num == 1 else f"{base_page_url}&page={page_num}"
    print(f"\n--- Fetching search results page {page_num}: {page_url} ---")
    cards = get_listing_urls(page_url)
    if not cards:
        print("  -> No listings returned from this page; stopping pagination.")
        break

    for card in cards:
        if len(valid_listings) >= TARGET_VALID_LISTINGS:
            break

        url = card.get("url")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        print(f"\n--- Processing listing {len(valid_listings)+1}/{TARGET_VALID_LISTINGS}: {url} ---")
        listing_data = scrape_details_and_prices(url, months_to_check, year_to_check)
        listing_data["image"] = card.get("image")

        if has_none(listing_data):
            print("  -> Listing missing data; skipping and continuing to next listing/page.")
            # continue to next card (we'll keep paging until we reach TARGET_VALID_LISTINGS)
            continue

        valid_listings.append(listing_data)
        # polite pause between listings
        human_pause(0.4, 0.9)

    page_num += 1
    # small pause between pages
    human_pause(0.8, 1.4)

if len(valid_listings) < TARGET_VALID_LISTINGS:
    print(f"\nWarning: only collected {len(valid_listings)} valid listings after paging to {page_num-1}.")

# Save results
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(valid_listings, f, ensure_ascii=False, indent=2)

print(f"\nDone! Saved {len(valid_listings)} valid records to {OUTPUT_FILE}")
driver.quit()
