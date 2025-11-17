from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

OUTPUT_FILE = "näytönohjaimet.txt"

def scrape(url, label, file):
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)

    driver.get(url)
    title = driver.title
    
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # let new content load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    names = driver.find_elements(By.CLASS_NAME, "product-box-name")
    prices = driver.find_elements(By.CLASS_NAME, "price__amount")

    file.write(f"{title}\n")
    file.write(f"Löytyi {len(names)} {label}:\n")

    print(title)
    print(f"Löytyi {len(names)} {label}:")

    for name, price in zip(names, prices):
        line = f"- {name.text.strip()} | Hinta: {price.text.strip()}\n"
        file.write(line)
        print(line.strip())

    file.write("\n \n \n")
    print()
    driver.quit()


def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        scrape(
            "https://www.jimms.fi/fi/Product/List/000-29T/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-5070",
            "RTX 5070 Näytönohjainta",
            file
        )
        scrape(
            "https://www.jimms.fi/fi/Product/List/000-29S/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-5070-ti",
            "RTX 5070 Ti Näytönohjainta",
            file
        )
        scrape(
            "https://www.jimms.fi/fi/Product/List/000-29P/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-5080",
            "RTX 5080 Näytönohjainta",
            file
        )


if __name__ == "__main__":
    main()
    print(f"Tulokset tallennettu tiedostoon: {OUTPUT_FILE}")
