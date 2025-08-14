import json
from pathlib import Path
from .schema import AnalysisBundle, ArticleAnalysis
from .summarizer import summarize_text
from .entities import extract_entities

def analyze_research_file(file_path: Path):
    """Read research JSON and produce analysis."""
    data = json.loads(file_path.read_text(encoding="utf-8"))
    query = data.get("query", "")
    articles_data = data.get("articles", [])

    analyzed_articles = []
    for art in articles_data:
        text = art.get("text", "")
        summary = summarize_text(text)
        entities = extract_entities(text)
        keywords = list(set(
            word.lower()
            for word in text.split()
            if len(word) > 6
        ))[:10]

        analyzed_articles.append(ArticleAnalysis(
            title=art.get("title"),
            url=art.get("url"),
            summary=summary,
            entities=entities,
            keywords=keywords
        ))

    return AnalysisBundle(query=query, articles=analyzed_articles)
