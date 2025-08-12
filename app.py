# app.py
import streamlit as st
from scraper import manual_scrape, ai_scrape
import os
if not os.path.exists("/home/adminuser/.cache/ms-playwright"):
    from playwright.sync_api import sync_playwright
    import subprocess
    subprocess.run(["playwright", "install", "chromium"])


st.title("InfoParse - Web Scraper")

option = st.radio("Choose scraping mode:", ["Manual (Tag/Class)", "AI Q&A"])

url = st.text_input("Enter URL (with http/https):")

if option == "Manual (Tag/Class)":
    tag = st.text_input("Enter HTML tag (e.g., p, div):")
    class_name = st.text_input("Enter class name (optional):")

    if st.button("Scrape"):
        if url and tag:
            results = manual_scrape(url, tag, class_name)
            st.write(results)
        else:
            st.warning("Please provide both a valid URL and tag.")

elif option == "AI Q&A":
    question = st.text_input("Enter your question:")
    if st.button("Ask AI"):
        if url and question:
            results = ai_scrape(url, question)
            for res in results:
                st.write(f"Answer: {res['answer']}")
                st.write(f"Score: {res['score']:.4f}")
        else:
            st.warning("Please provide both a valid URL and question.")
