from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


OUTPUT_FILE = "asunnot_yhdistetty.json"

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)


####################################################################
# YHTEINEN APUTOIMINTO: hyväksy cookie-iframe
####################################################################

def accept_cookies():
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[src*='consent']")
        ))
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Hyväksy')]")
        ))
        btn.click()
        print("✔ Evästeet hyväksytty")
    except:
        print("ℹ Ei cookie-iframea")
    finally:
        driver.switch_to.default_content()


####################################################################
# 1) OIKOTIE – 20 uusinta
####################################################################

def scrape_oikotie():
    print("\n=== Haetaan Oikotien 20 uusinta ===")

    url = (
        "https://asunnot.oikotie.fi/myytavat-asunnot"
        "?cardType=100"
        "&buildingType%5B%5D=2&buildingType%5B%5D=4&buildingType%5B%5D=8"
        "&buildingType%5B%5D=32&buildingType%5B%5D=128&buildingType%5B%5D=64"
        "&locations=%5B%5B9,7,%22Kymenlaakso%22%5D%5D"
        "&price%5Bmax%5D=100000&price%5Bmin%5D=45000"
        "&size%5Bmin%5D=55"
    )

    driver.get(url)
    time.sleep(2)
    accept_cookies()

    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cards-v3__card")))
    except:
        print("❌ Oikotieltä ei löytynyt ilmoituksia")
        return []

    listings = driver.find_elements(By.CSS_SELECTOR, "div.cards-v3__card")[:20]
    results = []

    for card in listings:
        try:
            link = card.find_element(By.CSS_SELECTOR, "a.ot-card-v3").get_attribute("href")
            title = card.find_element(By.CSS_SELECTOR, ".card-v3-text-container__text").text

            spans = card.find_elements(By.CSS_SELECTOR,
                                       "span.card-v3-text-container__heading.heading--title-2")
            price = spans[0].text if len(spans) > 0 else ""
            size = spans[1].text if len(spans) > 1 else ""

            results.append({
                "site": "Oikotie",
                "title": title,
                "price": price,
                "size": size,
                "link": link
            })

        except Exception:
            continue

    print(f"✔ Oikotie: haettu {len(results)} ilmoitusta")
    return results


####################################################################
# 2) ETUOVI – 20 uusinta
####################################################################

def scrape_etuovi():
    print("\n=== Haetaan Etuoven 20 uusinta ===")

    url = (
    "https://www.etuovi.com/myytavat-asunnot?haku=M2367606769"
    )

    driver.get(url)
    time.sleep(3)
    accept_cookies()

    # Kortit = Etuoven MUI-kortit
    try:
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.MuiCard-root")
        ))
    except:
        print("❌ Etuovesta ei löytynyt ilmoituksia")
        return []

    cards = driver.find_elements(By.CSS_SELECTOR, "div.MuiCard-root")[:20]
    results = []

    for card in cards:
        try:
            # LINKKI
            try:
                link = card.find_element(
                    By.CSS_SELECTOR, "a[href*='/kohde/']"
                ).get_attribute("href")
            except:
                continue

            # OTSIKKO – <h3> sisältää osoitteen
            try:
                title = card.find_element(
                    By.CSS_SELECTOR,
                    "h3.MuiTypography-root.MuiTypography-body1"
                ).text.strip()
            except:
                title = "Ilmoitus"

            # HINTA
            try:
                price = card.find_element(
                    By.XPATH,
                    ".//p[contains(., 'Hinta')]/following-sibling::span"
                ).text.replace("\xa0", "").strip()
            except:
                price = ""

            # KOKO (m²)
            try:
                size = card.find_element(
                    By.XPATH,
                    ".//span[contains(., 'm²')]"
                ).text.replace("\xa0", "").strip()
            except:
                size = ""

            results.append({
                "site": "Etuovi",
                "title": title,
                "price": price,
                "size": size,
                "link": link
            })

        except Exception:
            continue

    print(f"✔ Etuovi: haettu {len(results)} ilmoitusta")
    return results


####################################################################
# SUORITA SCRAPET + TALLENNUS
####################################################################

try:
    oikotie_data = scrape_oikotie()
    etuovi_data = scrape_etuovi()

    all_data = oikotie_data + etuovi_data

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print("\n==============================")
    print(f" Tallennettu yhteensä {len(all_data)} ilmoitusta")
    print(f" → {OUTPUT_FILE}")
    print("==============================\n")

finally:
    driver.quit()
























