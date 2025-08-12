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
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    # Run AI model
    results = qa_pipeline(question=query, context=text)

    # Debug print (remove in production)
    print("DEBUG AI output:", results)

    # Handle different formats
    if isinstance(results, dict):
        # For QA pipelines
        return [results.get("answer", ""), f"Score: {results.get('score', 'N/A')}"]
    elif isinstance(results, list):
        # For text-generation or classification pipelines
        extracted = []
        for item in results:
            if isinstance(item, dict):
                extracted.append(item.get("generated_text") or item.get("label") or str(item))
        return extracted
    else:
        return [str(results)]


    # AI: classify each block of text against the query
    results = classifier(candidates, [query], multi_label=False)

    # Keep only highly relevant matches
    filtered = []
    for text, score in zip(results["sequence"], results["scores"]):
        if score > 0.6:  # threshold for relevance
            filtered.append(text)

    return filtered
