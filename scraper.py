# scraper.py
# scraper.py
from scraper_requests_html import fetch_with_requests_html
from scraper_playwright import fetch_with_playwright
from transformers import pipeline

# AI model pipeline (for Q&A)
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

SCRAPER_MODE = "playwright"  # Change to "requests_html" to switch

def manual_scrape(url, tag, class_name=None):
    if SCRAPER_MODE == "playwright":
        return fetch_with_playwright(url, tag, class_name)
    else:
        return fetch_with_requests_html(url, tag, class_name)

def ai_scrape(url, question):
    if SCRAPER_MODE == "playwright":
        page_text = fetch_with_playwright(url)
    else:
        page_text = fetch_with_requests_html(url)

    if not page_text or len(page_text.strip()) < 20:
        return "No meaningful content found."

    result = qa_pipeline({
        "context": page_text,
        "question": question
    })

    return {
        "answer": result["answer"],
        "score": result["score"]
    }
