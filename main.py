import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

OUTPUT_FILE = "NäytönohjainMonitori.json"


def clean_price(price_text):
    price_text = price_text.replace("€", "").strip()
    price_text = price_text.replace(" ", "").replace(",", ".")
    try:
        return float(price_text)
    except ValueError:
        return None


def scrapegpu(url):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)

    driver.get(url)
    time.sleep(2)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    products = driver.find_elements(By.CLASS_NAME, "product-box")

    items = []
    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, "product-box-name").text.strip()
            price_raw = product.find_element(By.CLASS_NAME, "price__amount").text.strip()
            price = clean_price(price_raw)

            link = product.find_element(By.CLASS_NAME, "js-gtm-product-link").get_attribute("href")

            if price is not None:
                items.append({
                    "name": name,
                    "price": price,
                    "link": link
                })
        except:
            continue

    driver.quit()
    return items


def scrapemonitor(url):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)

    driver.get(url)
    time.sleep(2)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    products = driver.find_elements(By.CLASS_NAME, "product-box")

    items = []
    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, "product-box-name").text.strip()
            price_raw = product.find_element(By.CLASS_NAME, "price__amount").text.strip()
            price = clean_price(price_raw)

            link = product.find_element(By.CLASS_NAME, "js-gtm-product-link").get_attribute("href")

            if price is not None:
                items.append({
                    "name": name,
                    "price": price,
                    "link": link
                })
        except:
            continue

    driver.quit()
    return items


def main():
    all_data = {}

    all_data["===========RTX 5070==========="] = scrapegpu(
        "https://www.jimms.fi/fi/Product/List/000-29T/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-5070?ob=4"
    )

    all_data["===========RTX 5070 TI==========="] = scrapegpu(
        "https://www.jimms.fi/fi/Product/List/000-29S/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-5070-ti?ob=4"
    )

    all_data["===========RTX 5080==========="] = scrapegpu(
        "https://www.jimms.fi/fi/Product/List/000-29P/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-5080?ob=4"
    )
    
    all_data["===========RX 9070==========="] = scrapegpu(
        "https://www.jimms.fi/fi/Product/List/000-29N/komponentit--naytonohjaimet--amd-radeon--rx-9000-sarja--rx-9070?ob=4"
    )
    
    all_data["===========RX 9070 XT==========="] = scrapegpu(
        "https://www.jimms.fi/fi/Product/List/000-29M/komponentit--naytonohjaimet--amd-radeon--rx-9000-sarja--rx-9070-xt?ob=4"
    )

    all_data["===========1440 Monitori==========="] = scrapemonitor(
        "https://www.jimms.fi/fi/Product/List/000-0KJ/oheislaitteet--naytot?ob=4&fq=QHD"
    )

    halvimmat = {}
    for category, items in all_data.items():
        if items:
            halvimmat_item = min(items, key=lambda x: x["price"])
            halvimmat[category] = halvimmat_item
        else:
            halvimmat[category] = None

    all_data["halvimmat"] = halvimmat

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print("\n===== 3 Halvinta Tuotetta Jokaisessa Kategoriassa =====")

    for category, items in all_data.items():
        if category == "halvimmat":
            continue

        print(f"\n{category}:")

        if not items:
            print("  Ei tuotteita")
            continue

        sorted_items = sorted(items, key=lambda x: x["price"])

        for i, item in enumerate(sorted_items[:3], start=1):
            print(f"  {i}. {item['name']} — {item['price']} €")


if __name__ == "__main__":
    main()
