# InfoParse AI - ZIP Deploy

This package is a Playwright + Transformers based Streamlit app that:
- Renders pages with Playwright (handles JS)
- Extracts candidate text blocks
- Scores and summarizes them based on a natural-language query

Files:
- app.py
- scraper.py
- ai_processor.py
- requirements.txt

## Quick local run
1. python -m venv venv
2. source venv/bin/activate   (or venv\Scripts\activate on Windows)
3. pip install -r requirements.txt
4. playwright install
5. streamlit run app.py

## Deploy on Streamlit Cloud
- Upload this repo as a ZIP or push to GitHub and connect to Streamlit Cloud.
- Note: first build will install Playwright browsers. Cold start may be slower.
