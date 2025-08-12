# app.py
import streamlit as st
from scraper import scrape_candidates
from ai_processor import score_texts_by_query, summarize_top_texts
import pandas as pd

st.set_page_config(page_title="InfoParse AI", layout="wide")
st.title("InfoParse AI — Natural Language Web Extractor")

st.markdown("""Enter a URL and a natural-language instruction like:
- "List product names and prices"
- "Show headlines and intros"
- "What jobs and internships are available?"
""")

col1, col2 = st.columns([3,1])
with col1:
    url = st.text_input("Website URL (include https://)", value="")
with col2:
    mode = st.selectbox("Output mode", ["List (ranked)", "Summarize", "Table/CSV"])

query = st.text_area("What do you want to extract? (plain English)", height=80, value="List the main headlines")

if st.button("Run"):
    if not url or not query:
        st.warning("Please provide both a URL and a query.")
    else:
        # basic URL normalization
        if not url.startswith("http"):
            url = "https://" + url

        st.info("Loading and rendering page (Playwright). This may take 5-20s on cold start.")
        try:
            candidates = scrape_candidates(url)
        except Exception as e:
            st.error(f"Failed to render page: {e}")
            candidates = []

        if not candidates:
            st.warning("No candidate text blocks found. The page may block headless browsers.")
        else:
            st.success(f"Found {len(candidates)} candidate blocks. Scoring by query...")
            scored = score_texts_by_query(candidates, query)

            # deduplicate by text snippet
            seen = set()
            deduped = []
            for c in scored:
                key = c["text"][:180]
                if key not in seen:
                    deduped.append(c)
                    seen.add(key)
            top = deduped[:25]

            if mode == "List (ranked)":
                st.subheader("Top matches")
                df = pd.DataFrame(top)
                if not df.empty:
                    df_display = df[[]].copy() if False else df
                    st.dataframe(df[["score","tag","selector","text"]].rename(columns={"text":"content"}), height=400)
                    csv_buf = df.to_csv(index=False)
                    st.download_button("Download CSV", csv_buf, file_name="infoparse_results.csv")
                else:
                    st.info("No results to show.")

            elif mode == "Summarize":
                st.subheader("Summary from top matches")
                texts = [c["text"] for c in top]
                summary = summarize_top_texts(texts)
                st.write(summary)
                st.markdown("**Top source snippets:**")
                for i,c in enumerate(top[:8],1):
                    st.markdown(f"**{i}.** (score={c['score']}) {c['text'][:400]}")
                df = pd.DataFrame(top)
                st.download_button("Download CSV", df.to_csv(index=False), file_name="infoparse_summary_sources.csv")

            elif mode == "Table/CSV":
                df = pd.DataFrame(top)
                st.subheader("Table view")
                if not df.empty:
                    st.dataframe(df[["tag","selector","score","text"]].rename(columns={"text":"content"}), height=400)
                    st.download_button("Download CSV", df.to_csv(index=False), file_name="infoparse_table.csv")
                else:
                    st.info("No table data.")
