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
    "page" : 1,                                         # change via params_set_page(a)
    "item__is_payment_ad" : "null",                     # change via params_set_nettimaksu(True)
    "item__avg_overall_rating_4" : 1,                   # change via params_set_require_4_stars(True)
    "attr__number_of_bedrooms[0]" : "null",             #
    "attr__number_of_bedrooms[1]" : "null",             # change via params_set_bedrooms(a)
    "attr__number_of_bedrooms[2]" : "null",             # or change via params_set_bedrooms_range(a,b)
    "attr__number_of_bedrooms[3]" : "null"              #
}

# --------------- params / muuttojen funktiot ---------------
def params_clean(): # PITÄÄ käyttää, muuten "item__is_payment_ad" menee päällä vaikka mikä value olis tilalla
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

def params_set_bedrooms_range(a,b):   # asettaa haettavan numeroalueen makuuhuoneen määrän varten
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
    params_clean()
    fetch_page(PARAMS)
