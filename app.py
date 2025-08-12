# app.py
import streamlit as st
from scraper import manual_scrape, ai_scrape

st.set_page_config(page_title="InfoParse", layout="wide")
st.title("📰 InfoParse - Web Data Extractor")

# Input method
mode = st.radio("Choose Extraction Mode", ["Manual HTML Scrape", "AI Q&A"])

# Shared inputs
url = st.text_input("Enter the URL:")

if mode == "Manual HTML Scrape":
    col1, col2 = st.columns(2)
    with col1:
        tag = st.text_input("HTML Tag (e.g., div, p, h1):", "p")
    with col2:
        class_name = st.text_input("Class Name (leave blank if none):", "")

    if st.button("Scrape Manually"):
        if url.strip():
            try:
                results = manual_scrape(url, tag, class_name if class_name else None)
                if results:
                    st.success(f"Found {len(results)} items.")
                    for r in results:
                        st.write("-", r)
                else:
                    st.warning("No matching elements found.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid URL.")

elif mode == "AI Q&A":
    query = st.text_input("Enter your question:")
    if st.button("Ask AI"):
        if url.strip() and query.strip():
            try:
                results = ai_scrape(url, query)
                for r in results:
                    st.write("-", r)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter both a URL and a question.")

