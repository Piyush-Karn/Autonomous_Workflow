# loader.py
import json
import re
import pandas as pd
from pathlib import Path

# Possible date fields to check in Analyst Agent output
DATE_FIELDS = [
    "published_date",
    "date",
    "publishedAt",
    "created_at",
    "scraped_at",
]

# Regex patterns to find dates in URLs
DATE_REGEXES = [
    r"(\d{4})[/-](\d{2})[/-](\d{2})",  # 2025-08-14 or 2025/08/14
    r"(\d{4})(\d{2})(\d{2})",          # 20250814
]

def load_analyst_json(file_path: Path, frequency="daily", top_k_keywords=0):
    """
    Reads Analyst Agent JSON output and aggregates to time series.
    Optionally includes top-K keyword counts as features.
    """
    data = json.loads(file_path.read_text(encoding="utf-8"))
    articles = data.get("articles", [])

    rows = []
    skipped_no_date = 0

    for art in articles:
        # Must have at least some summary or text to be valid
        if not art.get("summary") and not art.get("text", ""):
            continue

        date = _extract_date(art)
        if not date:
            skipped_no_date += 1
            continue

        kws = art.get("keywords", []) or []
        rows.append({
            "date": pd.to_datetime(date).normalize(),
            "keywords": kws,
        })

    if not rows:
        raise ValueError("No valid articles with dates found. Ensure Analyst JSON contains a valid date field or URL pattern.")

    df = pd.DataFrame(rows)

    # Aggregate article counts per date
    ts = df.groupby("date").size().rename("article_count").to_frame()

    # Resample to given frequency
    rule = "D" if frequency == "daily" else "W"
    ts = ts.resample(rule).sum().fillna(0)

    # Add keyword-based exogenous drivers
    if top_k_keywords > 0:
        all_keywords = df["keywords"].explode().dropna()
        if not all_keywords.empty:
            top_kw = all_keywords.value_counts().head(top_k_keywords).index.tolist()
            for kw in top_kw:
                kw_counts = df.assign(
                    match=df["keywords"].apply(lambda kws: kw in (kws or []))
                )
                kw_ts = kw_counts.groupby("date")["match"].sum()
                kw_ts = kw_ts.resample(rule).sum().reindex(ts.index, fill_value=0)
                col = f"kw_{_safe_col(kw)}_count"
                ts[col] = kw_ts

    if skipped_no_date:
        print(f"ℹ️ Skipped {skipped_no_date} articles with no resolvable date.")

    return ts


def _extract_date(art: dict):
    """Try multiple places to find a date, then fallback to URL parsing."""
    # 1) Check common date fields
    for f in DATE_FIELDS:
        v = art.get(f)
        if v:
            try:
                return pd.to_datetime(v).date()
            except Exception:
                pass

    # 2) Check nested metadata.date
    meta = art.get("metadata") or {}
    md = meta.get("date")
    if md:
        try:
            return pd.to_datetime(md).date()
        except Exception:
            pass

    # 3) Parse from URL
    url = art.get("url") or ""
    if url:
        for rgx in DATE_REGEXES:
            m = re.search(rgx, url)
            if m:
                try:
                    if len(m.groups()) == 3:
                        y, mth, d = m.groups()
                        return pd.to_datetime(f"{y}-{mth}-{d}").date()
                except Exception:
                    continue

    return None


def _safe_col(kw: str) -> str:
    """Sanitize keyword to safe column name."""
    s = re.sub(r"\s+", "_", kw.strip().lower())
    s = re.sub(r"[^a-z0-9_]+", "", s)
    return s[:60]  # limit to avoid overly long column names
