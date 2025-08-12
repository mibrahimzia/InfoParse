# scraper.py
from playwright.sync_api import sync_playwright
from transformers import pipeline
import os

# Load AI model once
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def fetch_with_playwright(url):
    with sync_playwright() as p:
        # Explicitly set Chromium executable path
        chromium_path = p.chromium.executable_path
        browser = p.chromium.launch(headless=True, executable_path=chromium_path)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        content = page.content()
        browser.close()
        return content

def manual_scrape(url, tag):
    from bs4 import BeautifulSoup
    html_content = fetch_with_playwright(url)
    soup = BeautifulSoup(html_content, "html.parser")
    elements = soup.find_all(tag)
    return [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]

def ai_scrape(url, question):
    from bs4 import BeautifulSoup
    html_content = fetch_with_playwright(url)
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(" ", strip=True)
    answer = qa_pipeline(question=question, context=text)
    return answer
