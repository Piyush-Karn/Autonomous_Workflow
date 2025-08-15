import json
import re
import pandas as pd
from pathlib import Path

def load_analyst_json(file_path: Path, frequency="daily", top_k_keywords=0, include_sentiment=True):
    """
    Reads Analyst Agent JSON output and aggregates to a time series.
    Uses 'published' from Analyst directly (no URL guessing).
    """
    data = json.loads(file_path.read_text(encoding="utf-8"))
    articles = data.get("articles", [])

    rows = []
    skipped_no_date = 0

    for art in articles:
        if not art.get("published"):
            skipped_no_date += 1
            continue
        kws = art.get("keywords", []) or []
        row = {"date": pd.to_datetime(art["published"]).normalize(),
               "keywords": kws}
        if include_sentiment:
            row["sentiment_score"] = float(art.get("sentiment_score") or 0.0)
            row["source_weight"] = float(art.get("source_weight") or 0.0)
        rows.append(row)

    if not rows:
        raise ValueError("No valid articles with 'published' dates found.")

    df = pd.DataFrame(rows)

    # Aggregate article counts
    ts = df.groupby("date").size().rename("article_count").to_frame()

    rule = "D" if frequency == "daily" else "W"
    ts = ts.resample(rule).sum().fillna(0)

    # Aggregate sentiment/source weight
    if include_sentiment:
        sent_ts = df.groupby("date")["sentiment_score"].mean()
        sw_ts = df.groupby("date")["source_weight"].mean()
        ts["avg_sentiment"] = sent_ts.resample(rule).mean().reindex(ts.index, fill_value=0)
        ts["avg_source_weight"] = sw_ts.resample(rule).mean().reindex(ts.index, fill_value=0)

    # Keyword-based features
    if top_k_keywords > 0:
        all_keywords = df["keywords"].explode().dropna()
        if not all_keywords.empty:
            top_kw = all_keywords.value_counts().head(top_k_keywords).index.tolist()
            for kw in top_kw:
                kw_counts = df.assign(
                    kw_count=df["keywords"].apply(lambda kws: sum(1 for k in (kws or []) if k == kw))
                )
                kw_ts = kw_counts.groupby("date")["kw_count"].sum()
                kw_ts = kw_ts.resample(rule).sum().reindex(ts.index, fill_value=0)
                ts[f"kw_{_safe_col(kw)}_count"] = kw_ts

    if skipped_no_date:
        print(f"ℹ️ Skipped {skipped_no_date} articles with no resolvable 'published' date.")

    return ts

def _safe_col(kw: str) -> str:
    """Sanitize keyword to safe column name for model features."""
    s = re.sub(r"\s+", "_", kw.strip().lower())
    s = re.sub(r"[^a-z0-9_]+", "", s)
    return s[:60]
