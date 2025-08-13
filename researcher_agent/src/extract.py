from bs4 import BeautifulSoup
from urllib.parse import urlparse
from newspaper import Article as NPArticle

def _clean_text(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)

def extract_with_newspaper(url: str, html: str):
    art = NPArticle(url=url, language='en')
    art.download(input_html=html)
    art.parse()
    try:
        art.nlp()
        summary = art.summary
    except:
        summary = None
    return {
        "title": art.title or None,
        "authors": art.authors or [],
        "published": str(art.publish_date) if art.publish_date else None,
        "top_image": art.top_image or None,
        "summary": summary,
        "text": _clean_text(art.text or "")
    }

def extract_with_bs4(html: str):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    title = soup.title.string.strip() if soup.title else None
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    return {"title": title, "authors": [], "published": None, "top_image": None, "summary": None, "text": _clean_text("\n".join(paragraphs))}

def domain_of(url: str):
    return urlparse(url).netloc
