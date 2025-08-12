# scraper.py
import requests
from bs4 import BeautifulSoup

def dynamic_search(soup, query):
    query_words = [w.strip().lower() for w in query.split() if w.strip()]
    scored = []

    for tag in soup.find_all(True):
        text = tag.get_text(strip=True)
        if not text:
            continue

        text_lower = text.lower()
        score = sum(word in text_lower for word in query_words)

        # Weight based on tag importance
        if tag.name in ["h1", "h2", "h3"]:
            score += 1
        if tag.name == "title":
            score += 2

        if score > 0:
            scored.append((score, text))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)
    return [t for s, t in scored]

def scrape_content(url, query):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # Run dynamic search
        results = dynamic_search(soup, query)

        return results if results else ["No relevant content found."]
    except Exception as e:
        return [f"Error: {e}"]
