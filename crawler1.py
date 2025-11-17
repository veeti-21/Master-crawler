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



def crawl():
    for z in range(3):
        webPage = ['gigantti.fi/gaming/pelinaytot?f=30831%3A2560x1440%7C3840x2160%7C3440x1440' , 'gigantti.fi/gaming/pelinaytot' , 'gigantti.fi/gaming/pelinaytot/page-2']
        currtime = datetime.datetime.now()
        epoch_time = calendar.timegm(currtime.timetuple())
        filename = f'result-{epoch_time}.json'
        opts = Options()
        opts.add_argument("-headless")
        driver = webdriver.Firefox(options=opts)
        driver.get(f'https://www.{webPage[z]}')
        #driver.get("https://www.gigantti.fi/gaming/pelinaytot")
        #driver.get("https://www.gigantti.fi/gaming/pelinaytot/page-2")
        original_size = driver.get_window_size()
        # ilman alempia selenium ei lataa kaikkia sivun elementtejä oikein
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)

        elementurl = driver.find_elements(By.CSS_SELECTOR, "li.group > a:nth-child(2)")
        elementname = driver.find_elements(By.CSS_SELECTOR, "li.group > a:nth-child(2) > div > div:nth-child(1) > h2:nth-child(2)") # selectorin "div" osasta piti ottaa nth-child pois että se hakee nimen ja hinnan oikein
        elementprice = driver.find_elements(By.CSS_SELECTOR, "li.group > a:nth-child(2) > div > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")


        print(webPage[z])
        for x in range (len(elementurl)):
        #        print(x)

            tmp1 = f"{elementname[x].get_attribute('textContent')}\n"
            tmp2 = f"{elementprice[x].text}\n"
            tmp3 = f"{elementurl[x].get_attribute('href')}\n\n"

            with open(filename, 'a', encoding='utf-8') as f: # tekee tiedoston ja lisää siihen tulokset 
                f.write(tmp1)
                f.write(tmp2)
                f.write(tmp3)
                print(tmp3)
                print(tmp2)
                print(tmp1) 
            #f.close()
        # printit testausta varten
            
        driver.quit()


crawl()