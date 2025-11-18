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


def scrapegpu(url, label):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)

    print(f"Etsitään: {label}")
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

    names = driver.find_elements(By.CLASS_NAME, "product-box-name")
    prices = driver.find_elements(By.CLASS_NAME, "price__amount")

    items = []
    for name, price in zip(names, prices):
        n = name.text.strip()
        p = clean_price(price.text.strip())
        if p is not None:
            items.append({
                "name": n,
                "price": p
            })

    driver.quit()
    return items


def scrapemonitor(url, label):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)

    print(f"Etsitään: {label}")
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

    names = driver.find_elements(By.CLASS_NAME, "product-box-name")
    prices = driver.find_elements(By.CLASS_NAME, "price__amount")

    items = []
    for name, price in zip(names, prices):
        n = name.text.strip()
        p = clean_price(price.text.strip())
        if p is not None:
            items.append({
                "name": n,
                "price": p
            })

    driver.quit()
    return items


def main():
    all_data = {}

    all_data["===========RTX 5070==========="] = scrapegpu(
        "https://www.jimms.fi/fi/Product/List/000-29T/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-5070?ob=4",
        "RTX 5070"
    )

    all_data["===========RTX 5070 TI==========="] = scrapegpu(
        "https://www.jimms.fi/fi/Product/List/000-29S/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-5070-ti?ob=4",
        "RTX 5070 Ti"
    )

    all_data["===========RTX 5080==========="] = scrapegpu(
        "https://www.jimms.fi/fi/Product/List/000-29P/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-5080?ob=4",
        "RTX 5080"
    )
    
    all_data["===========RX 9070 XT==========="] = scrapegpu(
        "https://www.jimms.fi/fi/Product/List/000-29M/komponentit--naytonohjaimet--amd-radeon--rx-9000-sarja--rx-9070-xt?ob=4",
        "RX 9070 XT"
    )

    all_data["===========1440 Monitori==========="] = scrapemonitor(
        "https://www.jimms.fi/fi/Product/List/000-0KJ/oheislaitteet--naytot?ob=4&fq=QHD",
        "1440 Monitori"
    )

    cheapest = {}
    for category, items in all_data.items():
        if items:
            cheapest_item = min(items, key=lambda x: x["price"])
            cheapest[category] = cheapest_item
        else:
            cheapest[category] = None

    all_data["cheapest"] = cheapest

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print("\n===== 3 HALVINTA TUOTETTA / KATEGORIA =====")

    for category, items in all_data.items():
        if category == "cheapest":
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
