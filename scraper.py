# scraper.py
from requests_html import HTMLSession
from transformers import pipeline

# Manual scraper that can handle basic JS
def manual_scrape(url, tag, class_name=None):
    session = HTMLSession()
    try:
        r = session.get(url)
        r.html.render(timeout=20)  # Render JavaScript
        if class_name:
            elements = r.html.find(f"{tag}.{class_name}")
        else:
            elements = r.html.find(tag)
        return [el.text for el in elements if el.text.strip()]
    except Exception as e:
        return [f"Error: {e}"]

# AI scraper using HuggingFace Q&A
def ai_scrape(url, query):
    session = HTMLSession()
    try:
        r = session.get(url)
        r.html.render(timeout=20)
        text_content = " ".join([el.text for el in r.html.find("*") if el.text.strip()])

        qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        result = qa(question=query, context=text_content)

        return [{"answer": result["answer"], "score": result["score"]}]
    except Exception as e:
        return [{"answer": f"Error: {e}", "score": 0}]
