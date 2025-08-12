# app.py
import streamlit as st
from scraper import scrape_content

st.set_page_config(page_title="ParseBot", page_icon="🔍", layout="wide")
st.title("🔍 ParseBot - Smart Web Content Extractor")

st.markdown("""
Enter a webpage URL and describe in plain English what you want to extract.  
Example: *"Get all article titles"* or *"Extract product names and prices"*.
""")

url = st.text_input("Enter webpage URL")
nl_query = st.text_area("What do you want to extract?", height=100)

if st.button("Scrape Data"):
    if not url.strip() or not nl_query.strip():
        st.error("Please enter both URL and query.")
    else:
        st.info("Scraping the webpage based on your query...")
        results = scrape_content(url, nl_query)

        if results and not results[0].startswith("Error:"):
            st.success(f"✅ Found {len(results)} relevant results.")
            for i, item in enumerate(results[:50], start=1):
                st.write(f"**{i}.** {item}")
        else:
            st.error(results[0] if results else "No results found.")
