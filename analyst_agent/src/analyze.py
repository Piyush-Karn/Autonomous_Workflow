# analyze.py
import json
from pathlib import Path

from .schema import AnalysisBundle, ArticleAnalysis
from .summarizer import summarize_text
from .entities import extract_entities

# NEW: RAKE import
from rake_nltk import Rake

def extract_keywords_rake(text: str, top_k: int = 10):
    """
    Extract top-K key phrases using RAKE.
    - Uses NLTK stopwords and punctuation filtering internally.
    - Returns phrases sorted by RAKE score (descending).
    """
    if not text or not text.strip():
        return []

    r = Rake()
    r.extract_keywords_from_text(text)
    ranked_phrases_with_scores = r.get_ranked_phrases_with_scores()

    top_phrases = [phrase for _, phrase in ranked_phrases_with_scores[:top_k]]


    seen = set()
    deduped = []
    for p in top_phrases:
        norm = p.strip().lower()
        if norm and norm not in seen:
            seen.add(norm)
            deduped.append(p.strip())
    return deduped

def analyze_research_file(file_path: Path):
    """Read research JSON and produce analysis."""
    data = json.loads(file_path.read_text(encoding="utf-8"))

    query = data.get("query", "")
    articles_data = data.get("articles", [])

    analyzed_articles = []

    for art in articles_data:
        text = art.get("text", "") or ""
        summary = summarize_text(text)
        entities = extract_entities(text)

        # UPDATED: Use RAKE instead of len(word) > 6
        keywords = extract_keywords_rake(text, top_k=10)

        analyzed_articles.append(ArticleAnalysis(
            title=art.get("title"),
            url=art.get("url"),
            summary=summary,
            entities=entities,
            keywords=keywords
        ))

    return AnalysisBundle(query=query, articles=analyzed_articles)
