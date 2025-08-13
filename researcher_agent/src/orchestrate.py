from typing import List
from .schema import Article, ResearchBundle
from .search import web_search
from .fetch import fetch_url
from .extract import extract_with_newspaper, extract_with_bs4, domain_of

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
        word_count=len(text.split()),
        status=status,
        error=error
    )

def research(query: str, limit: int = 8, take_first_n: int = 6) -> ResearchBundle:
    """
    Performs a web search for the given query, fetches articles, and extracts content.
    limit = number of search results to fetch.
    take_first_n = number of articles to process.
    """
    hits = web_search(query, max_results=limit)
    articles: List[Article] = []

    for hit in hits[:take_first_n]:
        html, err = fetch_url(hit["url"])
        if err:
            articles.append(_build_article(hit["url"], None, status="skipped", error=err))
            continue
        try:
            extracted = extract_with_newspaper(hit["url"], html)
            if not extracted.get("text"):
                extracted = extract_with_bs4(html)
        except Exception:
            extracted = extract_with_bs4(html)

        articles.append(_build_article(hit["url"], extracted))

    return ResearchBundle(query, articles)
