# app.py
import streamlit as st
import pandas as pd

from scraper import scrape_candidates
from nlp_utils import score_texts_by_query, summarize_texts, get_backend_status

st.set_page_config(page_title="InfoParse AI — PT only", layout="wide")
st.title("InfoParse AI — Natural Language Web Extractor (PyTorch-only)")

st.markdown(
    """
    This tool renders pages with Playwright (Chromium), extracts visible text blocks,
    matches them to your natural-language request, and (optionally) summarizes results
    with a **PyTorch-only** transformers pipeline. No TensorFlow imports.
    """
)

with st.expander("Backend status"):
    status = get_backend_status()
    st.json(status)

col1, col2 = st.columns([3,1])
with col1:
    url = st.text_input("Website URL (include https://)", value="")
with col2:
    mode = st.selectbox("Output mode", ["List (ranked)", "Summarize", "Table/CSV"])

query = st.text_area(
    "What do you want to extract? (plain English)",
    height=90,
    value="List the main headlines"
)

with st.expander("Advanced options"):
    top_k = st.number_input("How many top matches to keep", min_value=5, max_value=100, value=25, step=5)
    do_summary = st.checkbox("Use AI summarization (PyTorch)", value=(mode == "Summarize"))
    max_summary_tokens = st.slider("Summary max tokens (approx)", 64, 256, 120, step=8)

if st.button("Run"):
    if not url or not query:
        st.warning("Please provide both a URL and a query.")
        st.stop()

    if not url.startswith("http"):
        url = "https://" + url

    st.info("Rendering page with Playwright. First run can take longer (Chromium + model download).")
    try:
        candidates = scrape_candidates(url)
    except Exception as e:
        st.error(f"Failed to render or scrape: {e}")
        st.stop()

    if not candidates:
        st.warning("No candidate text blocks found. The page may block headless browsers or has minimal visible text.")
        st.stop()

    st.success(f"Found {len(candidates)} candidate blocks. Scoring by query...")
    scored = score_texts_by_query(candidates, query)

    # Deduplicate by first 180 chars
    seen = set()
    deduped = []
    for c in scored:
        k = c["text"][:180]
        if k not in seen:
            seen.add(k)
            deduped.append(c)
    top = deduped[:top_k]

    if mode == "List (ranked)":
        st.subheader("Top matches")
        df = pd.DataFrame(top)
        st.dataframe(
            df[["score", "tag", "selector", "text"]].rename(columns={"text": "content"}),
            height=420
        )
        st.download_button("Download CSV", df.to_csv(index=False), file_name="infoparse_results.csv")

    elif mode == "Summarize":
        st.subheader("Summary from top matches")
        texts = [c["text"] for c in top]
        summary = summarize_texts(texts, use_ai=do_summary, max_summary_tokens=max_summary_tokens)
        st.write(summary)

        st.markdown("**Top source snippets:**")
        for i, c in enumerate(top[:10], 1):
            st.markdown(f"**{i}.** (score={c['score']}) {c['text'][:500]}")

        df = pd.DataFrame(top)
        st.download_button("Download CSV", df.to_csv(index=False), file_name="infoparse_summary_sources.csv")

    elif mode == "Table/CSV":
        st.subheader("Table view")
        df = pd.DataFrame(top)
        if not df.empty:
            st.dataframe(
                df[["tag", "selector", "score", "text"]].rename(columns={"text": "content"}),
                height=420
            )
            st.download_button("Download CSV", df.to_csv(index=False), file_name="infoparse_table.csv")
        else:
            st.info("No table data.")
