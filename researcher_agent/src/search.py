from ddgs import DDGS
from urllib.parse import urlparse

def web_search(query: str, max_results: int = 10):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, region="in-en", safesearch="moderate", max_results=max_results))
    seen = set()
    unique = []
    for r in results:
        url = r.get("href") or r.get("url")
        if not url:
            continue
        key = urlparse(url)._replace(query="", fragment="").geturl()
        if key in seen:
            continue
        seen.add(key)
        unique.append({"title": r.get("title"), "url": url, "snippet": r.get("body")})
    return unique
