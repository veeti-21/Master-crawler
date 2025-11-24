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
import time


# webpage linkkien tilalla pitäisi toimia mikä tahansa gigantin sivu. 
webPage = ['gigantti.fi/gaming/tietokonekomponentit/naytonohjaimet-gpu' , 'gigantti.fi/gaming/tietokonekomponentit/naytonohjaimet-gpu/page-2' , 'gigantti.fi/gaming/tietokonekomponentit/naytonohjaimet-gpu/page-3' , 'gigantti.fi/gaming/pelinaytot?f=30831%3A2560x1440%7C3840x2160%7C3440x1440' , 'gigantti.fi/gaming/pelinaytot' , 'gigantti.fi/gaming/pelinaytot/page-2']


def crawl(*args):
        try:
                for z in range(len(webPage)):
                        # ottaa ajan, muuntaa sen epoch aikaan ja tallentaa tiedoston muodossa "result-xxxxxxxxxx.json". tiedoston tallennus tapahtuu kansioon jossa crawler on
                        currtime = datetime.datetime.now()
                        epoch_time = calendar.timegm(currtime.timetuple())
                        filename = f'result-{z}.json'
                        opts = Options()
                        opts.add_argument("--headless=new")
                        driver = webdriver.Firefox(options=opts)
                        print(f" crawlaus nro: {z + 1}")
                        driver.get(f'https://www.{webPage[z]}')

                        # odottaa että eväste banner latautuu sivulle
                        elementurl = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button.coi-banner__accept:nth-child(3)"))
                )
                        try:    # klikkaa eväste popupista "OK"
                                gdprbtn = driver.find_element(By.CSS_SELECTOR, "button.coi-banner__accept:nth-child(3)")
                                driver.execute_script("arguments[0].scrollIntoView(true);", gdprbtn)
                                gdprbtn.click()
                        except:
                                print("no gdpr button here")

                        # ilman alempia selenium ei lataa kaikkia sivun elementtejä oikein
                        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
                        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
                        driver.set_window_size(required_width, required_height)              

                        #elementprice = driver.find_elements(By.CSS_SELECTOR, "li.group > a > div > div > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
                        #elementurl = driver.find_elements(By.CSS_SELECTOR, "li.group > a:nth-child(2)")
                        elementname = driver.find_elements(By.CSS_SELECTOR, "li.group > a:nth-child(2) > div > div:nth-child(1) > h2:nth-child(2)") # selectorin "div" osasta piti ottaa nth-child pois että se hakee nimen ja hinnan oikein
                        # screenshot testausta varten, voi poistaa myöhemmin.
                        #driver.save_screenshot(f'screenie{z}.png')

                        print(webPage[z] , "\n\n\n\n\n\n\n") 
                        for x in range (len(elementname)):
                                        # tmp1 = nimi
                                        # tpm2 = hinta
                                        # tmp3 = linkki
                                # x + 1 koska gigantin sivun elementtien index alkaa ykkösestä.
                                # ei toimi kaikilla sivuilla koska ensimmäinen elementti on erilainen pelinäyttöjen ja näytönohjainten sivuilla
                                tmp1 = driver.find_element(By.CSS_SELECTOR, f"li:nth-child({x + 1}) > a:nth-child(2) > div > div:nth-child(1) > h2:nth-child(2)").text 
                                tmp2 = driver.find_element(By.CSS_SELECTOR, f"li.group:nth-child({x + 1}) > a > div > div > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)").text
                                tmp3 = driver.find_element(By.CSS_SELECTOR, f"li.group:nth-child({x + 1}) > a:nth-child(2)").get_attribute('href')
                                #tmp1 = f"{elementname[x].get_attribute('textContent')}"
                                #tmp1 = f"{elementname[x].text}"
                                #tmp2 = f"{elementprice[x].text}\n"
                                #tmp3 = f"{elementurl[x].get_attribute('href')}\n\n"
                                testjson = {
                                "nimi": tmp1,
                                "hinta": tmp2,
                                "linkki": tmp3
                                }
                                with open(filename, 'a', encoding='utf-8') as f: # tekee tiedoston ja lisää siihen tulokset. pitää vielä formatoida paremmin json/xml/csv muotoon.
                                        if x == 0:
                                                f.write("{")
                                        print(json.dumps(testjson, indent=4, separators=(",", ":")))
                                        
                                        f.write(f'"objekti{x}"')
                                        f.write(":[")
                                        f.write(json.dumps(testjson, indent=4, separators=(",", ":")))
                                        if x == len(elementname):
                                                f.write("]}")
                                        else:
                                                f.write("],")
                                        #TODO viimeisen loopin lopuksi vika f.write pitää kirjoittaa "]}" eikä "],"
                                        #TODO kaikki printit ja ylimääräiset importit pitää poistaa kun crawleri toimii
                                        #TODO pitää keksiä miten haetut tiedot siirretään tietokantaan/koontisivulle
                                        #TODO tietojen muuntaminen json/xml muotoon ja formatointi
                                        #TODO jos crawlerin ajamisen keskeyttää "ctrl + c" se jättää seleniumin firefox driverin taustalle päälle. pitää joko selvittää miten keskeytyksen saa tehtyä paremmin tai jollain tavalla lopettaa firefox prosessi kun crawleri "sammuu"
                                        f.close()
                        
                driver.quit()
        finally:
                driver.quit()


crawl()
