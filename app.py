# app.py
import streamlit as st
from scraper import manual_scrape

st.set_page_config(page_title="InfoParse", page_icon="🔍", layout="centered")

st.title("🔍 InfoParse - Playwright Scraper")
st.write("Enter a URL, HTML tag, and optional class name to scrape.")

url = st.text_input("Website URL", "")
tag = st.text_input("HTML Tag (e.g., div, p, h1)", "")
class_name = st.text_input("Class Name (optional)", "")

if st.button("Scrape"):
    if url.strip() == "" or tag.strip() == "":
        st.warning("Please enter both URL and HTML tag.")
    else:
        try:
            results = manual_scrape(url, tag, class_name if class_name else None)
            if results:
                st.success(f"Found {len(results)} elements:")
                for r in results:
                    st.write(r)
            else:
                st.info("No matching elements found.")
        except Exception as e:
            st.error(f"Error: {e}")

