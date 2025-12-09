
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import io
import json
import re
import datetime
import calendar

currtime = datetime.datetime.now()
epoch_time = calendar.timegm(currtime.timetuple())
filename = f'json-files/Auto-result.json'
opts = Options()
opts.add_argument("--headless=new")
driver = webdriver.Firefox(options=opts)
original_size = driver.get_window_size()
required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(required_width, required_height)
# nettisivu
webPage = ["https://www.nettiauto.com/hakutulokset?haku=P62829718&page=1", "https://www.nettiauto.com/hakutulokset?haku=P62829718&page=2"]


print("autojen haku")
for z in range(len(webPage)):# etsii tulokset sivustosta
        items = []

        print(f"autojen haku nro: {z + 1}")
        filename = rf'C:\crawlers\Master-crawler\json-files\autot-{z + 1}.json'
        driver.get(f"{webPage[z]}")
        elementname = driver.find_elements(By.CSS_SELECTOR, "#listingData > div.grid-x.cell.list-body-new.total-upsell-ad > div > div.product-card__body > div.product-card__info > h2")
        elementprice = driver.find_elements(By.CSS_SELECTOR, '#listingData > div.grid-x.cell.list-body-new > div > div.product-card__body > div.product-card__info > div:nth-child(2) > div')
        elementlink = driver.find_elements(By.CSS_SELECTOR, '#listingData > div.grid-x.cell.list-body-new > div > a')
       
        
        for x in range(len(elementname)):# ottaa tulokset
                
                tmp1 = f"{elementname[x].get_attribute("textContent")}" 
                tmp2 = f"{elementprice[x].get_attribute("innerText").replace("\u00a0", " ")}"
                tmp3 = f"{elementlink[x].get_attribute('href')}"
                
                testjson = {
                "nimi": tmp1,
                "hinta": tmp2,
                "linkki": tmp3,
                }

                items.append(
                        testjson
                )
        with open(filename, 'w', encoding='utf-8') as f: # lisää tulokset.
                f.writelines(json.dumps(items, ensure_ascii=False, indent=4, separators=(",", ":")))

                f.close()

driver.quit()
