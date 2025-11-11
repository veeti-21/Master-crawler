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
    "item_availability__date_from": "2026-06-01",
    "item_availability__date_to": "2026-06-07"
}

def input_date(date_from, date_to): # format vvvv-kk-pv

    global PARAMS

    PARAMS.update = {
    "item_availability__date_from": date_from,
    "item_availability__date_to": date_to
    }
    

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

    fetch_page()
