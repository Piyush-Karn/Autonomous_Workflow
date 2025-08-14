from typing import List
from .schema import Article, ResearchBundle
from .search import web_search
from .fetch import fetch_url
from .extract import extract_with_newspaper, extract_with_bs4, domain_of

def _infer_source_type(domain: str):
    if domain.endswith(".gov") or ".gov." in domain:
        return "government"
    if domain.endswith(".edu") or ".edu." in domain:
        return "academic"
    if any(x in domain for x in ["news", "times", "guardian", "bbc", "cnn"]):
        return "news"
    return "other"

def _build_article(url: str, extracted: dict, status="ok", error=None) -> Article:
    text = extracted.get("text", "") if extracted else ""
    return Article(
        title=extracted.get("title") if extracted else None,
        url=url,
        authors=extracted.get("authors") if extracted else [],
        published=extracted.get("published") if extracted else None,
        top_image=extracted.get("top_image") if extracted else None,
        summary=extracted.get("summary") if extracted else None,
        text=text,
        source=domain_of(url),
        source_type=_infer_source_type(domain_of(url)),
        word_count=len(text.split()),
        status=status,
        error=error,
        extra=extracted.get("extra", {}) if extracted else None
    )

def research(query: str, limit: int = 8, take_first_n: int = 6) -> ResearchBundle:
    print(f"🔍 Searching for '{query}' (limit={limit})...")
    hits = web_search(query, max_results=limit)
    print(f"✅ Found {len(hits)} results. Processing first {take_first_n}...")

    articles: List[Article] = []
    for i, hit in enumerate(hits[:take_first_n]):
        title = hit.get("title") or hit.get("url")
        print(f"[{i+1}/{take_first_n}] Processing: {title}")
        html, err = fetch_url(hit["url"])
        if err:
            print(f" ⚠️ Skipped ({err})")
            articles.append(_build_article(hit["url"], None, status="skipped", error=err))
            continue
        try:
            extracted = extract_with_newspaper(hit["url"], html)
            if not extracted.get("text"):
                print(" ℹ️ No text from Newspaper3k, falling back to BeautifulSoup...")
                extracted = extract_with_bs4(html, hit["url"])
        except Exception as e:
            print(f" ⚠️ Error in Newspaper3k ({e}), using BeautifulSoup...")
            extracted = extract_with_bs4(html, hit["url"])
        articles.append(_build_article(hit["url"], extracted))
        print(f" ✅ Done ({len(extracted.get('text', '').split())} words)")
    return ResearchBundle(query, articles)
