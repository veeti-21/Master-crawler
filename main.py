import requests
from bs4 import BeautifulSoup
import time
import urllib.parse


FILE_LOCATION = "C:\\Users\\jani\\Downloads\\useless-shit.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; VeetiBot/1.0; +https://example.com)"
}


BASE_URL = "https://www.nettimokki.com/vuokramokit/mokit-jarven-rannalla/"

PARAMS = {
    "item_availability__date_from": "2026-06-01",       # change via params_set_date(a,b)
    "item_availability__date_to": "2026-06-07",         # change via params_set_date(a,b)
    "page" : "null",                                    # change via params_set_page(a)
    "item__is_payment_ad" : "null",                     # change via params_set_nettimaksu(True)
    "item__avg_overall_rating_4" : "null",              # change via params_set_require_4_stars(True)
    "attr__number_of_bedrooms[0]" : "null",             #
    "attr__number_of_bedrooms[1]" : "null",             # change via params_set_bedrooms(a)
    "attr__number_of_bedrooms[2]" : "null",             # or change via params_set_bedrooms_range(a,b)
    "attr__number_of_bedrooms[3]" : "null",             #

    "attr__type_of_waters[0]" : "null",                 # 4503 = Järvi, 4504 = Meri, 4505 = Joki, 4507 = Lampi (???)
    "attr__type_of_waters[1]" : "null",                 #
    "attr__type_of_waters[2]" : "null",                 # change via params_set_water(Järvi = False, Meri = False, Joki = False, Lampi = False)
    "attr__type_of_waters[3]" : "null",                 #

    "attr__type_of_beach[0]" : "null",                 # 4503 = Järvi, 4504 = Meri, 4505 = Joki, 4507 = Lampi (???)
    "attr__type_of_beach[1]" : "null",                 #
    "attr__type_of_beach[2]" : "null",                 # change via params_set_water(Järvi = False, Meri = False, Joki = False, Lampi = False)
    "attr__type_of_beach[3]" : "null",                 #




}

# --------------- params / muuttojen funktiot ---------------
def params_clean(): # PITÄÄ käyttää, muuten nullit ovat literaaleja
    global PARAMS

    PARAMS = {k: v for k, v in PARAMS.items() if v != "null"}

def params_set_date(date_from, date_to): # format vvvv-kk-pv

    global PARAMS

    PARAMS.update({
    "item_availability__date_from": date_from,
    "item_availability__date_to": date_to
    })
    
def params_set_page(page): # menee asetetulle sivulle, ei tarkista onko olemassa jne, käytä for loopis tai jotai

    global PARAMS

    PARAMS.update({
    "page": page
    })

def params_set_nettimaksu(a): # tarvii True / False

    global PARAMS
    if a:
        PARAMS.update({
            "item__is_payment_ad" : 1
        })
    else:
        PARAMS.update({
            "item__is_payment_ad" : "null"
        })

def params_set_require_4_stars(a): # tarvii True / False
    global PARAMS
    if a:
        PARAMS.update({
            "item__avg_overall_rating_4" : 1
        })
    else:
        PARAMS.update({
            "item__avg_overall_rating_4" : "null"
        })

def params_set_bedrooms(a): # asettaa tarkan haettavan huoneitten määrän, esim 2 on vaan 2 makuuhuonetta ei enemmän ei vähemmän
    global PARAMS

    PARAMS.update({ # Tyhjentää vanhat pois 
        "attr__number_of_bedrooms[0]" : "null",
        "attr__number_of_bedrooms[1]" : "null",
        "attr__number_of_bedrooms[2]" : "null",
        "attr__number_of_bedrooms[3]" : "null",
    })

    PARAMS.update({ # Laittaa valitun huoneitten määrän
        "attr__number_of_bedrooms[0]": a
    })

def params_set_bedrooms_range(a,b): # asettaa haettavan numeroalueen makuuhuoneen määrän varten, esim 1,4 etsii kaikki paikat jossa on 1-4 huonetta
                                                # range 1-4
    global PARAMS
    if(a >= 4 or a <= 0 or b >= 4 or b <= 0):   # asettaa range 1-4 
        return "range is 1-4"
    
    PARAMS.update({                             # Tyhjentää vanhat pois 
        "attr__number_of_bedrooms[0]" : "null",
        "attr__number_of_bedrooms[1]" : "null",
        "attr__number_of_bedrooms[2]" : "null",
        "attr__number_of_bedrooms[3]" : "null",
    })

    if(a<b):                                    # tarkista numerojärjestys
        for i in range(0, b-a+1):
            k = f"attr__number_of_bedrooms[{i}]"

            PARAMS.update({ 
                k : a+i,
            })
    else:
        for i in range(0, a-b+1):
            k = f"attr__number_of_bedrooms[{i}]"
            
            PARAMS.update({ 
                k : a+i,
            })

def params_set_water(Järvi = False, Meri = False, Joki = False, Lampi = False): # asettaa halutut vesistön tyyppi parametrit
    
    global PARAMS

    PARAMS.update({ # Tyhjentää vanhat pois 
        "attr__type_of_waters[0]" : "null",                 
        "attr__type_of_waters[1]" : "null",                 
        "attr__type_of_waters[2]" : "null",                 
        "attr__type_of_waters[3]" : "null",                 
    })

    if(Järvi):
        PARAMS.update({ 
            "attr__type_of_waters[0]" : 4503,                         
        })

    if(Meri):
        PARAMS.update({ 
            "attr__type_of_waters[1]" : 4504,                         
        })

    if(Joki):
        PARAMS.update({ 
            "attr__type_of_waters[2]" : 4505,                         
        })

    if(Lampi):
        PARAMS.update({ 
            "attr__type_of_waters[3]" : 4507,                         
        })

def params_set_beach(Oma = False, Jaettu = False, Käyttöoikeus_rantaan = False, Käyttöoikeus_vesialueisiin = False): # asettaa halutut ranta parametrit
    global PARAMS

    PARAMS.update({
        "attr__type_of_beach[0]" : "null",                 
        "attr__type_of_beach[1]" : "null",                 
        "attr__type_of_beach[2]" : "null",                 
        "attr__type_of_beach[3]" : "null", 

    })

    if(Oma):
        PARAMS.update({
            "attr__type_of_beach[0]" : "own_beach"
        })
    if(Jaettu):
        PARAMS.update({
            "attr__type_of_beach[1]" : "shared_beach"
        })
    if(Käyttöoikeus_rantaan):
        PARAMS.update({
            "attr__type_of_beach[2]" : "permission_to_use_beach"
        })
    if(Käyttöoikeus_vesialueisiin):
        PARAMS.update({
            "attr__type_of_beach[3]" : "permission_to_use_waterways"
        })


# ---------------------------------------------------------


def fetch_page(params=PARAMS, base_url=BASE_URL):
    

    if params:
        query_string = urllib.parse.urlencode(params, safe='/', encoding='utf-8')
        url = f"{base_url}?{query_string}"
        print(query_string)
        print(url)
    else:
        url = base_url
    print(f"Fetching URL: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        html = resp.text
        with open(FILE_LOCATION, "w", encoding="utf-8") as f:
            f.write(html)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")


if __name__ == "__main__":
    params_set_water(False,True,False,True)
    params_set_bedrooms_range(1,2)
    params_set_beach(True,False,True,False)

    params_clean()
    fetch_page(PARAMS)
