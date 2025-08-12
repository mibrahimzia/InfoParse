# ai_processor.py - lightweight scoring and summarization
from transformers import pipeline
from typing import List, Dict
import math

# Use a lighter summarizer to reduce memory/startup
try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except Exception as e:
    print("Warning: summarizer model failed to load:", e)
    summarizer = None

def score_texts_by_query(candidates: List[Dict], query: str) -> List[Dict]:
    q_tokens = [t.lower() for t in query.split() if len(t) > 2]
    scored = []
    for c in candidates:
        text = c.get("text", "").lower()
        hits = sum(1 for w in q_tokens if w in text)
        prop = hits / (len(q_tokens) + 1)
        tag_w = 0
        if c["tag"] in ("h1", "h2", "h3"):
            tag_w += 0.8
        if c["tag"] == "a":
            tag_w += 0.2
        length_score = min(1.0, math.log(max(1, len(text.split()))) / 5.0)
        score = prop * 3.0 + tag_w + length_score
        c2 = c.copy()
        c2["score"] = round(score, 4)
        scored.append(c2)
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

def summarize_top_texts(top_texts: List[str], max_summary_tokens=120) -> str:
    if not top_texts:
        return "No content to summarize."
    combined = "\n\n".join(top_texts[:6])
    if summarizer:
        try:
            res = summarizer(combined, max_length=max_summary_tokens, min_length=30, do_sample=False)
            return res[0]["summary_text"]
        except Exception as e:
            print("Summarizer error:", e)
            return combined[:800] + ("..." if len(combined) > 800 else "")
    else:
        return combined[:800] + ("..." if len(combined) > 800 else "")
