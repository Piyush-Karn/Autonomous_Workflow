from bs4 import BeautifulSoup
from urllib.parse import urlparse
from newspaper import Article as NPArticle
import re
import pandas as pd
from datetime import datetime

# Month lookup for text/URL parsing
MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12
}

def _clean_text(text: str) -> str:
    """Normalize whitespace in extracted article text."""
    lines = [ln.strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)

def _extract_date_from_meta(soup: BeautifulSoup):
    """Try to get publish date from HTML meta tags."""
    meta_props = [
        {"attr": "property", "name": "article:published_time"},
        {"attr": "name", "name": "pubdate"},
        {"attr": "name", "name": "publishdate"},
        {"attr": "property", "name": "og:pubdate"},
        {"attr": "name", "name": "date"},
        {"attr": "itemprop", "name": "datePublished"},
    ]
    for mp in meta_props:
        tag = soup.find("meta", {mp["attr"]: mp["name"]})
        if tag and tag.get("content"):
            try:
                return str(pd.to_datetime(tag["content"]).date())
            except Exception:
                pass
    return None

def _extract_date_from_text(soup: BeautifulSoup):
    """Look for date-like patterns in visible HTML text."""
    text = soup.get_text(separator=" ")

    # DD Month YYYY or Month DD YYYY
    m1 = re.search(r"\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*[,\s]+(\d{4})", text, re.I)
    if m1:
        day, mon, year = m1.groups()
        try:
            return str(datetime(int(year), MONTH_MAP[mon.lower()[:3]], int(day)).date())
        except Exception:
            pass

    m2 = re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+(\d{1,2})[,\s]+(\d{4})", text, re.I)
    if m2:
        mon, day, year = m2.groups()
        try:
            return str(datetime(int(year), MONTH_MAP[mon.lower()[:3]], int(day)).date())
        except Exception:
            pass

    # Month YYYY only → default to first day of month
    m3 = re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*[,\s]+(\d{4})", text, re.I)
    if m3:
        mon, year = m3.groups()
        try:
            return str(datetime(int(year), MONTH_MAP[mon.lower()[:3]], 1).date())
        except Exception:
            pass

    return None

def _extract_date_from_url(url: str):
    """Check for date patterns inside the URL."""
    date_patterns = [
        r"(\d{4})[/-](\d{2})[/-](\d{2})",  # 2025-08-14 or 2025/08/14
        r"(\d{4})(\d{2})(\d{2})",          # 20250814
    ]
    for pat in date_patterns:
        match = re.search(pat, url)
        if match:
            try:
                y, m, d = match.groups()
                return str(datetime(int(y), int(m), int(d)).date())
            except Exception:
                continue

    # YYYY-monthname or monthname-YYYY
    for mon_name, mon_num in MONTH_MAP.items():
        m1 = re.search(rf"{mon_name}[-/](\d{{4}})", url, re.I)
        if m1:
            try:
                return str(datetime(int(m1.group(1)), mon_num, 1).date())
            except Exception:
                pass
        m2 = re.search(rf"(\d{{4}})[-/]{mon_name}", url, re.I)
        if m2:
            try:
                return str(datetime(int(m2.group(1)), mon_num, 1).date())
            except Exception:
                pass

    return None

def robust_published_date(html: str, url: str):
    """Master function to try all date extraction fallbacks."""
    soup = BeautifulSoup(html, "lxml")
    return (
        _extract_date_from_meta(soup)
        or _extract_date_from_text(soup)
        or _extract_date_from_url(url)
        or str(datetime.utcnow().date())  # Fallback: today's date
    )

def extract_with_newspaper(url: str, html: str):
    """Extract article with Newspaper3k + robust date fallback."""
    art = NPArticle(url=url, language='en')
    art.download(input_html=html)
    art.parse()

    try:
        art.nlp()
        summary = art.summary
    except Exception:
        summary = None

    # Try Newspaper3k's publish_date first
    published_date = None
    if art.publish_date:
        published_date = str(art.publish_date.date())
    else:
        published_date = robust_published_date(html, url)

    return {
        "title": art.title or None,
        "authors": art.authors or [],
        "published": published_date,
        "top_image": art.top_image or None,
        "summary": summary,
        "text": _clean_text(art.text or ""),
        "extra": {
            "meta_keywords": _extract_meta_keywords(html)
        }
    }

def _extract_meta_keywords(html: str):
    soup = BeautifulSoup(html, "lxml")
    tag = soup.find("meta", attrs={"name": "keywords"})
    if tag and tag.get("content"):
        return [kw.strip() for kw in tag["content"].split(",")]
    return []

def extract_with_bs4(html: str, url: str):
    """Simpler BS4 extractor (fallback if Newspaper3k fails)."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    title = soup.title.string.strip() if soup.title else None
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    published_date = robust_published_date(html, url)
    return {
        "title": title,
        "authors": [],
        "published": published_date,
        "top_image": None,
        "summary": None,
        "text": _clean_text("\n".join(paragraphs)),
        "extra": {
            "meta_keywords": _extract_meta_keywords(html)
        }
    }

def domain_of(url: str):
    return urlparse(url).netloc
