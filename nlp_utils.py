# nlp_utils.py — PyTorch-only transformers with graceful fallback
import os
from typing import List, Dict
import math

# Force transformers to avoid TensorFlow/Flax imports entirely
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["TRANSFORMERS_NO_FLAX"] = "1"

# Try to import torch; if unavailable, we degrade gracefully
try:
    import torch  # noqa: F401
    HAS_TORCH = True
except Exception:
    HAS_TORCH = False

# summarizer pipeline (lazy)
_SUMMARIZER = None

def _load_summarizer():
    global _SUMMARIZER
    if _SUMMARIZER is not None:
        return _SUMMARIZER

    if not HAS_TORCH:
        _SUMMARIZER = None
        return None

    try:
        from transformers import pipeline
        # Smaller, faster summarizer; force PyTorch backend
        _SUMMARIZER = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            framework="pt"
        )
    except Exception as e:
        print("⚠️ Could not load summarizer (PyTorch):", e)
        _SUMMARIZER = None
    return _SUMMARIZER

def get_backend_status():
    """Return a small diagnostic blob for UI."""
    return {
        "torch_available": HAS_TORCH,
        "summarizer_loaded": _SUMMARIZER is not None,
        "env": {
            "TRANSFORMERS_NO_TF": os.environ.get("TRANSFORMERS_NO_TF", ""),
            "TRANSFORMERS_NO_FLAX": os.environ.get("TRANSFORMERS_NO_FLAX", ""),
        }
    }

def score_texts_by_query(candidates: List[Dict], query: str) -> List[Dict]:
    q_tokens = [t.lower() for t in query.split() if len(t) > 2]
    scored = []
    for c in candidates:
        text = c.get("text", "").lower()
        hits = sum(1 for w in q_tokens if w in text)
        prop = hits / (len(q_tokens) + 1)
        tag_w = 0.0
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

def _fallback_summarize(texts: List[str], limit_chars: int = 800) -> str:
    if not texts:
        return "No content to summarize."
    combined = "\\n\\n".join(texts[:6])
    if len(combined) <= limit_chars:
        return combined
    return combined[:limit_chars] + "..."

def summarize_texts(top_texts: List[str], use_ai: bool = True, max_summary_tokens: int = 120) -> str:
    if not top_texts:
        return "No content to summarize."

    if use_ai:
        summarizer = _load_summarizer()
        if summarizer is not None:
            try:
                combined = "\\n\\n".join(top_texts[:6])
                res = summarizer(
                    combined,
                    max_length=max_summary_tokens,
                    min_length=32,
                    do_sample=False
                )
                return res[0]["summary_text"]
            except Exception as e:
                return f"(AI summarizer error — falling back)\\n\\n{_fallback_summarize(top_texts)}"
    # fallback
    return _fallback_summarize(top_texts)
