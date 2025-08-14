# analyze.py
import json
from pathlib import Path
from typing import Optional
from datetime import datetime
import logging

from .schema import AnalysisBundle, ArticleAnalysis
from .summarizer import summarize_text
from .entities import extract_entities
from .normalizer import normalize_text, normalize_list
from .validators import validate_article

# Default: use RAKE
from rake_nltk import Rake
# Optional: YAKE fallback
try:
    import yake
    YAKE_AVAILABLE = True
except ImportError:
    YAKE_AVAILABLE = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def extract_keywords_rake(text: str, top_k: int = 10):
    """Extract top-K key phrases using RAKE with NLTK stopwords."""
    if not text or not text.strip():
        return []

    text = normalize_text(text)

    r = Rake()
    r.extract_keywords_from_text(text)
    ranked_phrases = r.get_ranked_phrases_with_scores()
    phrases = [p for _, p in ranked_phrases[:top_k]]
    return normalize_list(phrases)


def extract_keywords_yake(text: str, top_k: int = 10):
    """Optional YAKE-based keyword extraction."""
    if not YAKE_AVAILABLE:
        logger.warning("YAKE not installed; falling back to RAKE.")
        return extract_keywords_rake(text, top_k)

    kw_extractor = yake.KeywordExtractor(lan="en", top=top_k)
    keywords = [kw for kw, _ in kw_extractor.extract_keywords(text)]
    return normalize_list(keywords)


def analyze_research_file(file_path: Path, keyword_method: str = "rake"):
    """
    Main Analyst Agent step:
    - Validates input articles
    - Extracts summaries, entities, keywords
    - Logs metrics for monitoring
    """
    raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    query = raw_data.get("query", "")
    articles_data = raw_data.get("articles", [])

    analyzed_articles = []
    total_entities = 0
    total_keywords = 0

    for idx, art in enumerate(articles_data, start=1):
        if not validate_article(art):
            logger.warning(f"Skipping invalid article at index {idx}: {art}")
            continue

        text = normalize_text(art.get("text", ""))

        summary = summarize_text(text)
        entities = extract_entities(text)
        keyword_extractor = extract_keywords_yake if keyword_method == "yake" else extract_keywords_rake
        keywords = keyword_extractor(text, top_k=10)

        total_entities += sum(len(v) for v in entities.values())
        total_keywords += len(keywords)

        analyzed_articles.append(ArticleAnalysis(
            title=normalize_text(art.get("title")),
            url=art.get("url"),
            summary=summary,
            entities=entities,
            keywords=keywords
        ))

    logger.info(f"✅ Processed {len(analyzed_articles)} valid articles.")
    logger.info(f"📊 Avg Entities/Article: {total_entities / max(1, len(analyzed_articles)):.2f}")
    logger.info(f"📊 Avg Keywords/Article: {total_keywords / max(1, len(analyzed_articles)):.2f}")

    return AnalysisBundle(query=query, articles=analyzed_articles)
