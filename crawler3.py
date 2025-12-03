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
  host="localhost",
  user="root",
  password="",
  database="vimmdb"
)


# webpage linkkien tilalla pitäisi toimia mikä tahansa gigantin sivu. 
# crawler2 hakee näytönohjaimia
# webPage listaan voi lisätä lisää linkkejä jos tarvitsee

webPage = 'https://vimm.net/vault/N64'
# ottaa ajan, muuntaa sen epoch aikaan ja tallentaa tiedoston muodossa "result-xxxxxxxxxx.json". tiedoston tallennus tapahtuu kansioon jossa crawler on
currtime = datetime.datetime.now()
epoch_time = calendar.timegm(currtime.timetuple())
opts = Options()
opts.add_argument("--headless=new")
opts.add_argument('--disable-blink-features=AutomationControlled')
alphlist = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def crawl(*args):

        for z in range(len(alphlist)):
                driver = webdriver.Firefox(options=opts)
                
                sivu = f'{webPage}/{alphlist[z]}'
                filename = f'result-{z}.json'
                print(f" crawlaus nro: {z + 1}")
                driver.get(sivu)

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

                time.sleep(1)
                try:

                        elementnames = driver.find_elements(By.CSS_SELECTOR, "table.rounded > tbody:nth-child(2) > tr > td")
                        print(len(elementnames))
                except: 
                        elementnames = driver.find_elements(By.CSS_SELECTOR, "table.rounded:nth-child(3) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(1) > a:nth-child(1)")

                print(sivu , "\n\n\n\n\n\n\n")
                
                for x in range (len(elementnames)):

                        # x + 1 koska html-elementtien index alkaa ykkösestä.
                        try:
                                nimi = driver.find_element(By.CSS_SELECTOR, f"table.rounded > tbody:nth-child(2) > tr:nth-child({x + 1}) > td:nth-child(1) > a").get_attribute('innerText') 
                        except: 
                                print("lmao")
                                pass
                        finally:
                                pass

                        try:
                                linkki = driver.find_element(By.CSS_SELECTOR, f"table.rounded > tbody > tr:nth-child({x + 1}) > td:nth-child(1) > a").get_attribute('href')
                        except:
                                print("lol")
                                pass
                        finally:
                                pass
 

                        tmp4 = time.strftime('%Y-%m-%d %H:%M')
                        mycursor = mydb.cursor()

                        sql = "INSERT INTO games_list (vimm_nimi, vimm_linkki, vimm_aika) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE vimm_nimi=VALUES(vimm_nimi), vimm_linkki=VALUES(vimm_linkki), vimm_aika=VALUES(vimm_aika)"
                        val = (nimi, linkki, tmp4)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        print(mycursor.rowcount, "record inserted.")
                       
                        # alempi kommentoitu koodi tallentaa samat tiedot .json tiedostoon. .json tiedostossa url encoding(ä = %C3%A4, ö = %C3%B6 tyylinen) ja se pitää muuntaa erikseen utf-8 jos sitä haluaa käyttää muuhun kuin testaukseen
                        """testjson = {
                        "nimi": nimi,
                        #"hinta": hinta,
                        "linkki": linkki
                        }
                        with open("vimmgames", 'a', encoding='utf-8') as f: # tekee tiedoston ja lisää siihen tulokset. pitää vielä formatoida paremmin json/xml/csv muotoon.
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