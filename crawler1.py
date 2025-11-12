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
# ottaa ajan, muuntaa sen epoch aikaan ja tallentaa tiedoston muodossa "result-xxxxxxxxxx.json". tiedoston tallennus tapahtuu kansioon jossa crawler on
currtime = datetime.datetime.now()
epoch_time = calendar.timegm(currtime.timetuple())
filename = f'result-{epoch_time}.json'

opts = Options()
opts.add_argument("-headless")
driver = webdriver.Firefox(options=opts)
driver.get("https://www.gigantti.fi/gaming/pelinaytot")
original_size = driver.get_window_size()
# ilman alempia selenium ei lataa kaikkia sivun elementtejä oikein
required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(required_width, required_height)

elementname = driver.find_elements(By.CSS_SELECTOR, "li.group > a:nth-child(2) > div:nth-child(3) > div:nth-child(1) > h2:nth-child(2)")
elementprice = driver.find_elements(By.CSS_SELECTOR, "li.group > a > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")

for x in range (len(elementprice)):
    tmp1 = f"{elementname[x].text}\n"
    tmp2 = f"{elementprice[x].text}\n\n" # elementprice ottaa väärästä elementistä numeron, jos tuotteella on alennus

    if "näyttö" in tmp1 and "€" in tmp2: # and "€" saattaa olla turha
            with open(filename, 'a', encoding='utf-8') as f: # tekee tiedoston ja lisää siihen tulokset 
                f.write(tmp1)
                f.write(tmp2)
    print(tmp2)
    print(tmp1)
driver.quit()
