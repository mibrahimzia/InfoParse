# scraper.py
import subprocess
import os
from playwright.sync_api import sync_playwright

# Auto-install chromium if missing
PLAYWRIGHT_CACHE = os.path.expanduser("~/.cache/ms-playwright")
if not os.path.exists(PLAYWRIGHT_CACHE) or not os.listdir(PLAYWRIGHT_CACHE):
    try:
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        print("⚠️ Failed to auto-install Chromium:", e)

def manual_scrape(url, tag, class_name=None):
    """Scrape elements by tag and optional class using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        if class_name:
            selector = f"{tag}.{class_name}"
        else:
            selector = tag

        elements = page.query_selector_all(selector)
        results = [el.inner_text().strip() for el in elements if el.inner_text().strip()]

        browser.close()
        return results
