# InfoParse AI (PyTorch-only)

This Streamlit app renders pages with Playwright, extracts visible text blocks,
ranks them by your natural-language query, and optionally summarizes results
using Hugging Face Transformers in **PyTorch-only** mode — TensorFlow is disabled.

## Project layout
```
.
├── app.py
├── scraper.py
├── nlp_utils.py
├── requirements.txt
├── runtime.txt            # Forces Python 3.11 on Streamlit Cloud
├── packages.txt           # System libs for Chromium
└── .streamlit/
    └── config.toml
```

## Local run
```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
playwright install
streamlit run app.py
```

## Streamlit Cloud
- Push these files to GitHub and deploy.
- First build may take longer (Chromium + model download).
- `runtime.txt` pins Python 3.11 to ensure PyTorch wheels exist.
- If the app ever complains about missing browsers, it auto-runs
  `playwright install chromium` at runtime as a fallback.

## Notes
- If PyTorch is unavailable in an environment, the app **gracefully falls back**
  to a simple extractive summarization (no errors).
- You can toggle summarization in the UI. When disabled, results still show
  ranked matches and CSV export.
