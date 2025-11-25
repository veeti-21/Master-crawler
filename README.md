# Master-crawler

Jokaiselle itemille voidaan ottaa pari tekijää, jotka tekevät yhteistyössä tietojen haun

Tiedot mitä halutaan koota crawlattuna:

nettiautosta uusi auto (speksit myöhemmin)
oikotieltä uusi koti (speksit myöhemmin)
verkkokaupoista uusi näytönohjain (nykyinen 3070) + uusi 1440p näyttö
vuokralle lomamökki kesälle 2026 viikoksi
lomamatka kesälle 2026 / hiihtolomalle (vko 9)

# Testaus-crawler

# huom.

## firefox webdriver tekee uuden "rust_mozprofile" nimisen tiedoston "C:\Users\username\AppData\Local\Temp" kansioon. driver.quit() pitäisi poistaa ne muttei tunnu toimivan.

Varmista että windowsissa on laitettu päälle powershell scriptien ajo
**windows 11**
asetukset -> järjestelmä -> lisäasetukset -> terminal kohdasta powershell suorittamiskäytäntö päälle
**windows 10**
asetukset -> päivittäminen ja suojaus -> kehittäjille -> powershell -> powershell suorittamiskäytäntö päälle

cd c:\\_repo_/_crawlerin-tiedostosijainti_
powershellissä, cmd:ssä tai visual studion terminaalissa
tekee ja aloittaa virtual enviromentit:

python -m venv .venv
.venv\Scripts\Activate.ps1

jos alempi ei toimi aja powershell/cmd adminina.
pitää ajaa nämä komennot poweshellissä, powershelliin voi kopioida molemmat samaan aikaan CMD vaatii rivin kerrallaan:

python -m pip install --upgrade pip
pip install --upgrade selenium

crawleri ajetaan komennolla:
python crawler1.py

crawler tallentaa result.json tiedostoon haetun datan
pitää jossain vaiheessa lisätä gitignore jossa result tiedostot pois gitistä
