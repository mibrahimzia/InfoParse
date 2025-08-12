# scraper.py
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Load AI model once at startup (BART for zero-shot classification)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def manual_scrape(url, tag, class_name):
    """Scrape using HTML tag and optional class name."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all(tag, class_=class_name if class_name else None)
    return [el.get_text(strip=True) for el in elements]
'''_____________________________________________________________________________________________________'''
     # Auto-add schema if missing
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all(tag, class_=class_name)
    return [r.get_text(strip=True) for r in results]
'''_______________________________________________________________________________________________________'''

def ai_scrape(url, query):
    """Scrape all visible text and use AI to filter relevant content."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get all text from tags that might contain relevant content
    candidates = []
    for tag in ["p", "h1", "h2", "h3", "li", "span"]:
        for el in soup.find_all(tag):
            text = el.get_text(strip=True)
            if text and len(text.split()) > 2:
                candidates.append(text)

    # AI: classify each block of text against the query
    results = classifier(candidates, [query], multi_label=False)

    # Keep only highly relevant matches
    filtered = []
    for text, score in zip(results["sequence"], results["scores"]):
        if score > 0.6:  # threshold for relevance
            filtered.append(text)

    return filtered
