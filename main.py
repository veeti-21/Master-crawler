import requests
from bs4 import BeautifulSoup
import time
import urllib.parse


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; VeetiBot/1.0; +https://example.com)"
}


BASE_URL = "https://www.nettimokki.com/vuokramokit/mokit-jarven-rannalla/"
PARAMS = {
    "item_availability__date_from": "2026-06-01",
    "item_availability__date_to": "2026-06-07"
}

def fetch_page(params=PARAMS, base_url=BASE_URL):
    if params:
        query_string = urllib.parse.urlencode(params, safe='/', encoding='utf‑8')
        url = f"{base_url}?{query_string}"
    else:
        url = base_url
    print(f"Fetching URL: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        html = resp.text
        print(html)  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

if __name__ == "__main__":

    fetch_page()
