# scraper.py - Playwright-only rendering and candidate extraction
import subprocess
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from typing import List, Dict

# Ensure playwright browsers installed at runtime if missing (safe fallback)
PLAYWRIGHT_CACHE = os.path.expanduser("~/.cache/ms-playwright")
if not os.path.exists(PLAYWRIGHT_CACHE) or not os.listdir(PLAYWRIGHT_CACHE):
    try:
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        print("Warning: playwright install failed at runtime:", e)

def _stealth_page_setup(page):
    """Apply simple stealth tricks to make Playwright appear less bot-like."""
    try:
        page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})
        page.evaluate(
            """() => {
                Object.defineProperty(navigator, 'webdriver', {get: () => false});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
            }"""
        )
    except Exception:
        pass

def scrape_candidates(url: str, timeout_ms: int = 60000) -> List[Dict]:
    """Return candidate text blocks from the rendered page: [{tag, text, selector}]."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                                                 "AppleWebKit/537.36 (KHTML, like Gecko) " 
                                                 "Chrome/116.0 Safari/537.36"))
        page = context.new_page()
        _stealth_page_setup(page)
        try:
            page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except PlaywrightTimeoutError:
                pass

            tags = ["h1", "h2", "h3", "p", "li", "a", "span", "div"]
            candidates = []
            for tag in tags:
                els = page.query_selector_all(tag)
                for el in els:
                    try:
                        txt = el.inner_text().strip()
                    except Exception:
                        txt = ""
                    if txt and len(txt) > 15:
                        try:
                            cls = el.get_attribute("class") or ""
                            cls = cls.split()[0] if cls.strip() else ""
                            sel = f"{tag}.{cls}" if cls else tag
                        except Exception:
                            sel = tag
                        candidates.append({"tag": tag, "text": txt, "selector": sel})
        finally:
            try:
                context.close()
                browser.close()
            except Exception:
                pass
    return candidates
