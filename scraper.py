# scraper.py
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from playwright.sync_api import sync_playwright

# Initialize AI model (can be changed to another open-source one)
try:
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
except Exception as e:
    qa_pipeline = None
    print("Warning: AI model could not be loaded:", e)


def format_url(url):
    """Ensure URL starts with http or https"""
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url


   

def fetch_page_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        content = page.content()
        text = page.inner_text("body")
        browser.close()
    return text




def manual_scrape(url, tag, class_name):
    """Manual HTML scraping based on tag and class"""
    url = format_url(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    elements = soup.find_all(tag, class_=class_name)
    return [el.get_text(strip=True) for el in elements]


def ai_scrape(url, query):
    """AI-assisted scraping and Q&A"""
    url = format_url(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    if qa_pipeline is None:
        return ["AI model not available"]

    try:
        results = qa_pipeline(question=query, context=text)
    except Exception as e:
        return [f"Error running AI model: {e}"]

    # Debug output (optional)
    print("DEBUG AI output:", results)

    # Handle possible formats
    if isinstance(results, dict):
        return [results.get("answer", "No answer found"),
                f"Score: {results.get('score', 'N/A')}"]
    elif isinstance(results, list):
        extracted = []
        for item in results:
            if isinstance(item, dict):
                extracted.append(item.get("generated_text") or item.get("label") or str(item))
        return extracted
    else:
        return [str(results)]

