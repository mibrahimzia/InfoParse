# scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_content(url, tag, css_class=""):
    """Scrape content from a given URL based on tag and optional class."""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        if css_class.strip():
            elements = soup.find_all(tag, class_=css_class)
        else:
            elements = soup.find_all(tag)

        return [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]
    except Exception as e:
        return [f"Error: {e}"]
