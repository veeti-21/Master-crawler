
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
filename = f'Auto-result.json'
opts = Options()
opts.add_argument("--headless=new")
driver = webdriver.Firefox(options=opts)
original_size = driver.get_window_size()
required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(required_width, required_height)

webPage = ["https://www.nettiauto.com/hakutulokset?haku=P62829718&page=1", "https://www.nettiauto.com/hakutulokset?haku=P62829718&page=2"]

with open(filename, 'w', encoding='utf-8') as f:# tekee tyhjän tai tyhjentää tiedoston
        f.writelines("")
f.close()

for z in range(len(webPage)):
        driver.get(f"{webPage[z]}")
        elementname = driver.find_elements(By.CSS_SELECTOR, "#listingData > div.grid-x.cell.list-body-new.total-upsell-ad > div > div.product-card__body > div.product-card__info > h2")
        elementprice = driver.find_elements(By.CSS_SELECTOR, '#listingData > div.grid-x.cell.list-body-new > div > div.product-card__body > div.product-card__info > div:nth-child(2) > div')
        elementlink = driver.find_elements(By.CSS_SELECTOR, '#listingData > div.grid-x.cell.list-body-new > div > a')
       
        
        for x in range(len(elementname)):
                
                tmp1 = f"{elementname[x].get_attribute("textContent")}\n"
                tmp2 = f"{elementprice[x].get_attribute("innerText")}\n"
                tmp3 = f"{elementlink[x].get_attribute('href')}\n\n"
                
                testjson = {
                "nimi": tmp1,
                "hinta": tmp2,
                "linkki": tmp3,
                }

                with open(filename, 'a', encoding='utf-8') as f: # lisää tulokset.
                        if x == 0 and z == 0:
                                f.writelines("{")
                                        
                                        
                        print(json.dumps(testjson, indent=4, separators=(",", ":")))
                                        
                        f.writelines(f'"objekti{x}-{z}"')
                        f.writelines(":[")
                        f.writelines(json.dumps(testjson, indent=4, separators=(",", ":")))
                        if x == len(elementname) - 1 and z == 1:
                                f.writelines("]\n}")
                        else:
                                f.writelines("],")
                                
                
                f.close()

driver.quit()
#jostain syystä ei laita hintaa tai nimeä joillekin tuloksille