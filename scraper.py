# scraper.py
from playwright.sync_api import sync_playwright
from transformers import pipeline

def fetch_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        content = page.content()
        text = page.inner_text("body")
        browser.close()
        return text

def manual_scrape(url, tag, class_name=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        if class_name:
            selector = f"{tag}.{class_name}"
        else:
            selector = tag
        elements = page.query_selector_all(selector)
        results = [el.inner_text() for el in elements if el.inner_text().strip()]
        browser.close()
        return results

def ai_scrape(url, query):
    text_content = fetch_page_content(url)
    qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    result = qa(question=query, context=text_content)
    return [{"answer": result["answer"], "score": result["score"]}]
