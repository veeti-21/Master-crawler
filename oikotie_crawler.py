from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import re  

OUTPUT_FILE = "json-files/asunnot_yhdistetty.json"
OPERA_BINARY = r"C:\selenium_drive\chrome-win64\chrome-win64\chrome.exe"
CHROMEDRIVER_PATH = r"C:\selenium_drive\chromedriver-win64\chromedriver-win64\chromedriver.exe"

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

def accept_cookies():
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='consent']")))
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Hyväksy')]")))
        btn.click()
    except:
        pass
    finally:
        driver.switch_to.default_content()

def scrape_oikotie():
    url = "https://asunnot.oikotie.fi/myytavat-asunnot?cardType=100&buildingType%5B%5D=2&buildingType%5B%5D=4&buildingType%5B%5D=8&buildingType%5B%5D=32&buildingType%5B%5D=128&buildingType%5B%5D=64&locations=%5B%5B9,7,%22Kymenlaakso%22%5D%5D&price%5Bmax%5D=100000&price%5Bmin%5D=45000&size%5Bmin%5D=55"
    driver.get(url)
    time.sleep(2)
    accept_cookies()
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cards-v3__card")))
    except:
        return []
    listings = driver.find_elements(By.CSS_SELECTOR, "div.cards-v3__card")[:20]
    results = []
    for card in listings:
        try:
            link = card.find_element(By.CSS_SELECTOR, "a.ot-card-v3").get_attribute("href")
            title = card.find_element(By.CSS_SELECTOR, ".card-v3-text-container__text").text
            spans = card.find_elements(By.CSS_SELECTOR, "span.card-v3-text-container__heading.heading--title-2")
            price = spans[0].text if len(spans) > 0 else ""
            size = spans[1].text if len(spans) > 1 else ""
            results.append({"site": "Oikotie", "title": title, "price": price, "size": size, "link": link})
        except:
            continue
    return results

def scrape_etuovi():
    url = "https://www.etuovi.com/myytavat-asunnot?haku=M2367606769"
    driver.get(url)
    time.sleep(3)
    accept_cookies()
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.MuiPaper-root")))
    except:
        return []
    cards = driver.find_elements(By.CSS_SELECTOR, "a.MuiPaper-root")[:20]
    results = []
    for card in cards:
        try:
            link = card.get_attribute("href")
            if "/kohde/" not in link:
                continue
            try:
                title = card.find_element(By.CSS_SELECTOR, "p.MuiTypography-h6").text.strip()
            except:
                title = ""
            try:
                price = card.find_element(By.CSS_SELECTOR, "p.MuiTypography-h5").text.strip()
            except:
                price = ""
            size = ""
            for elem in card.find_elements(By.XPATH, ".//*"):
                txt = elem.text.strip()
                if "m²" in txt or "m2" in txt:
                    match = re.search(r'\d+(?:[.,]\d+)?\s?m[²2]', txt)
                    if match:
                        size = match.group(0).replace(',', '.')
                        break
            results.append({"site": "Etuovi", "title": title, "price": price, "size": size, "link": link})
        except:
            continue
    return results

try:
    all_data = scrape_oikotie() + scrape_etuovi()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
finally:
    driver.quit()






















