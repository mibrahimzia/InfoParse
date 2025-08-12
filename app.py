# app.py
import streamlit as st
from scraper import manual_scrape, ai_scrape

st.set_page_config(page_title="InfoParse", layout="wide")
st.title("🔍 InfoParse — Smart Web Data Extractor")

mode = st.radio("Choose Mode", ["Manual (HTML Tag + Class)", "AI (Natural Language)"])

url = st.text_input("Enter the webpage URL:")

if mode == "Manual (HTML Tag + Class)":
    tag = st.text_input("HTML tag (e.g., p, div, h1)")
    class_name = st.text_input("HTML class (optional)")
    if st.button("Scrape Data"):
        if url and tag:
            with st.spinner("Scraping..."):
                results = manual_scrape(url, tag, class_name)
            if results:
                st.success(f"Found {len(results)} results")
                for r in results:
                    st.write(f"- {r}")
            else:
                st.warning("No results found. Check the tag/class.")

elif mode == "AI (Natural Language)":
    query = st.text_input("What do you want to find on this page? (e.g., latest news headlines)")
    if st.button("Scrape Data with AI"):
        if url and query:
            with st.spinner("AI is searching for relevant content..."):
                results = ai_scrape(url, query)
            if results:
                st.success(f"Found {len(results)} relevant matches")
                for r in results:
                    st.write(f"- {r}")
            else:
                st.warning("No relevant results found.")
