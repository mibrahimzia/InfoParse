# scraper_requests_html.py
from requests_html import HTMLSession

def fetch_with_requests_html(url, tag=None, class_name=None):
    session = HTMLSession()
    r = session.get(url)
    try:
        r.html.render(timeout=20)  # runs JS
    except Exception as e:
        print("JS render failed:", e)

    if tag:
        if class_name:
            elements = r.html.find(f"{tag}.{class_name}")
        else:
            elements = r.html.find(tag)
        return [el.text for el in elements]
    else:
        return r.html.text
