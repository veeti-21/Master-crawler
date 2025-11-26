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
import mysql.connector 

mydb = mysql.connector.connect(
  host="placeholder",
  user="placeholder",
  password="placeholder",
  database="placeholder"
)



# webpage linkkien tilalla pitäisi toimia mikä tahansa gigantin sivu. 
# crawler2 hakee näytönohjaimia
# webPage listaan voi lisätä lisää linkkejä jos tarvitsee

webPage = ['gigantti.fi/gaming/tietokonekomponentit/naytonohjaimet-gpu?f=31620%3A%255B16%252C32%255D&f=30831%3A7680%2520x%25204320&f=33706%3AGeForce%2520RTX%252050%2520Series']
# ottaa ajan, muuntaa sen epoch aikaan ja tallentaa tiedoston muodossa "result-xxxxxxxxxx.json". tiedoston tallennus tapahtuu kansioon jossa crawler on
currtime = datetime.datetime.now()
epoch_time = calendar.timegm(currtime.timetuple())
opts = Options()
opts.add_argument("--headless=new")
opts.add_argument('--disable-blink-features=AutomationControlled')


def crawl(*args):

        for z in range(len(webPage)):
                driver = webdriver.Firefox(options=opts)

                filename = f'result-{z}.json'
                print(f" crawlaus nro: {z + 1}")
                driver.get(f'https://www.{webPage[z]}')

                # odottaa että eväste banner latautuu sivulle, TODO tekeekö elementurl mitään?
                elementurl = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.coi-banner__accept:nth-child(3)"))
        )
                try:    # klikkaa eväste popupista "OK"
                        gdprbtn = driver.find_element(By.CSS_SELECTOR, "button.coi-banner__accept:nth-child(3)")
                        driver.execute_script("arguments[0].scrollIntoView(true);", gdprbtn)
                        gdprbtn.click()
                        print("gdpr nappia painettu")
                except:
                        print("no gdpr button here")
                # ilman alempia selenium ei lataa kaikkia sivun elementtejä oikein
                required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
                required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
                driver.set_window_size(required_width, required_height)              

                #elementprice = driver.find_elements(By.CSS_SELECTOR, "li.group > a > div > div > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
                #elementurl = driver.find_elements(By.CSS_SELECTOR, "li.group > a:nth-child(2)")
                time.sleep(5)
                try:
                        elementnames = driver.find_elements(By.CSS_SELECTOR, "li > a:nth-child(2) > div > div:nth-child(1) > h2:nth-child(2)")
                except: 
                        elementnames = driver.find_elements(By.CSS_SELECTOR, "li > a:nth-child(2) > div > div:nth-child(1) > h2:nth-child(2)")

                print(webPage[z] , "\n\n\n\n\n\n\n")
                
                for x in range (len(elementnames)):
                        # nimi= nimi
                        # tpm2 = hinta
                        # linkki = linkki
                        # x + 1 koska html-elementtien index alkaa ykkösestä.
                        try:
                                nimi= driver.find_element(By.CSS_SELECTOR, f"li.pt-4:nth-child({x + 1}) > a:nth-child(2) > div > div:nth-child(1) > h2:nth-child(2)").text 
                        except: 
                                nimi= driver.find_element(By.CSS_SELECTOR, f"li.group:nth-child({x}) > a:nth-child(2) > div > div:nth-child(1) > h2:nth-child(2)").text 
                        finally:
                                pass
                        try:
                                hinta= driver.find_element(By.CSS_SELECTOR, f"li.group:nth-child({x + 1}) > a > div > div > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)").text
                        except:
                                hinta= driver.find_element(By.CSS_SELECTOR, f"li.pt-4:nth-child({x}) > a > div > div > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)").text
                        finally:
                                pass
                        try:
                                linkki = driver.find_element(By.CSS_SELECTOR, f"li.group:nth-child({x + 1}) > a:nth-child(2)").get_attribute('href')
                        except:
                                linkki = driver.find_element(By.CSS_SELECTOR, f"li.pt-4:nth-child({x}) > a:nth-child(2)").get_attribute('href')
                        finally:
                                pass
 

                        tmp4 = time.strftime('%Y-%m-%d %H:%M')
                        mycursor = mydb.cursor()

                        sql = "INSERT INTO gpu (gpu_nimi, gpu_hinta, gpu_linkki, gpu_aika) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE gpu_nimi=VALUES(gpu_nimi), gpu_linkki=VALUES(gpu_linkki), gpu_aika=VALUES(gpu_aika)"
                        val = (nimi, hinta, linkki, tmp4)
                        mycursor.execute(sql, val)
                        mydb.commit()

                        print(mycursor.rowcount, "record inserted.")
                       
                        # alempi kommentoitu koodi tallentaa samat tiedot .json tiedostoon. .json tiedostossa url encoding(ä = %C3%A4, ö = %C3%B6 tyylinen) ja se pitää muuntaa erikseen utf-8 jos sitä haluaa käyttää muuhun kuin testaukseen
                        """testjson = {
                        "nimi": nimi,
                        "hinta": hinta,
                        "linkki": linkki
                        }
                        with open(filename, 'a', encoding='utf-8') as f: # tekee tiedoston ja lisää siihen tulokset. pitää vielä formatoida paremmin json/xml/csv muotoon.
                                if x == 0:
                                        f.writelines("{")
                                print(x)
                                
                                f.writelines(f'"objekti{x}"')
                                f.writelines(":[")
                                f.writelines(json.dumps(testjson, indent=4, separators=(",", ":")))
                                if x == len(elementnames) - 1:
                                        f.writelines("]\n}")
                                else:
                                        f.writelines("],")

                                f.close()"""
                driver.close()


        # driver.quit()
        # driver.close()
crawl()


#TODO kaikki printit ja ylimääräiset importit pitää poistaa kun crawleri toimii
#TODO jos crawlerin ajamisen keskeyttää "ctrl + c" se jättää seleniumin firefox prosessin taustalle päälle. ylimääräiset prosessit pitää sulkea tehtävänhallinnasta.
#TODO firefox webdriver tekee uuden "rust_mozprofile" nimisen tiedoston "C:\Users\username\AppData\Local\Temp" kansioon. driver.quit() pitäisi poistaa ne muttei tunnu toimivan.
#TODO tällä hetkellä jos crawlerin ajaa useaan kertaan json ei ole validia, koska edellisen crawlauksen päätteeksi tiedostoon tulee "[}" pääte. tämä ei haittaa jos tiedot lisätään suoraan tietokantaan.
#TODO tietokannan "browser display trasnformation" asetuksia pitää tutkia tarkemmin jos on aikaa
#TODO 