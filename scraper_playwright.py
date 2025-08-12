'''
# scraper_playwright.py
from playwright.sync_api import sync_playwright

def fetch_with_playwright(url, tag=None, class_name=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        if tag:
            selector = tag
            if class_name:
                selector += f".{class_name}"
            elements = page.locator(selector)
            results = [elements.nth(i).inner_text() for i in range(elements.count())]
            browser.close()
            return results
        else:
            text = page.inner_text("body")
            browser.close()
            return text
'''
