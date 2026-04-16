import json
from pathlib import Path
import logging
from collections import Counter
import re

from .schema import AnalysisBundle, ArticleAnalysis
from .summarizer import summarize_text
from .entities import extract_entities
from .normalizer import normalize_text, normalize_list
from .validators import validate_article
from .sentiment import get_sentiment
from .topics import assign_topics
from .patterns import detect_co_occurrences, analyze_temporal_trends, find_divergent_entities, calculate_historical_trend
from .synthesizer import synthesize_insights

from rake_nltk import Rake
try:
    import yake
    YAKE_AVAILABLE = True
except ImportError:
    YAKE_AVAILABLE = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------- Helpers ---------------- #

def _json_safe(obj):
    """Recursively ensure all dict keys are strings and values are JSON safe."""
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(x) for x in obj]
    return obj

def classify_source_type(source: str) -> str:
    """Categorise source domains into meaningful types."""
    s = (source or "").lower()
    if ".gov" in s:
        return "government"
    if ".edu" in s:
        return "academic"
    if any(n in s for n in ["times", "guardian", "reuters", "bbc", "indiatoday",
                            "hindustantimes", "ndtv", "forbes", "bloomberg"]):
        return "news"
    if any(n in s for n in ["marketresearch", "imarcgroup", "mordorintelligence",
                            "maximizemarketresearch", "researchandmarkets"]):
        return "market_research"
    if any(n in s for n in ["blog", "wordpress", "medium.com"]):
        return "blog"
    return "other"

def clean_keywords(keywords):
    """Remove punctuation, percent markers & duplicates from keyword list."""
    cleaned = []
    for kw in keywords:
        if not kw:
            continue
        k = kw.strip().lower()
        k = re.sub(r"\(\+?\d+[%]?\)", "", k)              # remove (+75%) patterns
        k = re.sub(r"[\(\)\[\]\{\}%]", "", k)             # remove leftover brackets/percents
        k = re.sub(r"\s{2,}", " ", k)                     # collapse spaces
        k = k.strip(" ,.;:-_")
        if k and k not in cleaned:
            cleaned.append(k)
    return cleaned

# ---------------- Keyword extraction ---------------- #

def extract_keywords_rake(text: str, top_k: int = 10):
    if not text or not text.strip():
        return []
    text = normalize_text(text)
    r = Rake()
    r.extract_keywords_from_text(text)
    ranked_phrases = r.get_ranked_phrases_with_scores()
    phrases = [p for _, p in ranked_phrases[:top_k]]
    return normalize_list(phrases)

def extract_keywords_yake(text: str, top_k: int = 10):
    if not YAKE_AVAILABLE:
        logger.warning("YAKE not installed; falling back to RAKE.")
        return extract_keywords_rake(text, top_k)
    kw_extractor = yake.KeywordExtractor(lan="en", top=top_k)
    keywords = [kw for kw, _ in kw_extractor.extract_keywords(text)]
    return normalize_list(keywords)

# ---------------- Main analysis ---------------- #

def analyze_research_file(file_path: Path, keyword_method: str = "rake"):
    raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    query = raw_data.get("query", "")
    articles_data = raw_data.get("articles", [])

    analyzed_articles = []
    total_entities = Counter()
    keyword_counts = Counter()

    # Precompute topic clusters and names
    topic_labels, topic_map = assign_topics(
        [normalize_text(a.get("text", "")) for a in articles_data],
        num_clusters=5
    )

    for idx, art in enumerate(articles_data, start=1):
        if not validate_article(art):
            logger.warning(f"Skipping invalid article at index {idx}: {art.get('url')}")
            continue

        text = normalize_text(art.get("text", ""))
        summary = summarize_text(text)
        entities = extract_entities(text)

        # Keyword extraction
        keyword_extractor = extract_keywords_yake if keyword_method == "yake" else extract_keywords_rake
        keywords = clean_keywords(keyword_extractor(text, top_k=10))
        
        # Promote frequent ORG/PRODUCT entities to keyword list
        for label in ("ORG", "PRODUCT"):
            for ent in entities.get(label, []):
                term = normalize_text(ent)
                if term and term.lower() not in keywords:
                    keywords.append(term.lower())

        # Sentiment
        sentiment_score, sentiment_label = get_sentiment(text)

        # Source type & weighting
        stype = classify_source_type(art.get("source"))
        sw = {"government": 1.0, "news": 0.8, "academic": 0.8, "market_research": 0.7, "blog": 0.6}.get(stype, 0.5)

        # Aggregate entity stats
        for vals in entities.values():
            if isinstance(vals, list):
                total_entities.update([str(x) for x in vals if isinstance(x, str)])

        keyword_counts.update(keywords)

        # Build analysis object
        analyzed_articles.append(ArticleAnalysis(
            title=normalize_text(art.get("title")),
            url=art.get("url"),
            published=art.get("published"),
            source=art.get("source"),
            source_type=stype,
            summary=summary,
            entities=_json_safe(entities),
            keywords=keywords,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            topic_cluster=int(topic_labels[idx - 1]),
            source_weight=sw,
            extra=_json_safe(art.get("extra"))
        ))

    # Pattern Analysis
    patterns = {
        "co_occurrences": detect_co_occurrences(analyzed_articles),
        "temporal_trends": analyze_temporal_trends(analyzed_articles),
        "divergent_entities": find_divergent_entities(analyzed_articles),
        "historical_trend": calculate_historical_trend(analyzed_articles)
    }

    summary_meta = {
        "total_articles": int(len(analyzed_articles)),
        "avg_sentiment": float(sum(a.sentiment_score for a in analyzed_articles) / max(1, len(analyzed_articles))),
        "top_keywords": [[str(k), int(c)] for k, c in keyword_counts.most_common(10)],
        "top_entities": [[str(k), int(c)] for k, c in total_entities.most_common(10)],
        "articles_by_source_type": {
            str(k): int(v) for k, v in Counter(a.source_type for a in analyzed_articles).items()
        }
    }

    # Generate Narrative Insights
    bundle = AnalysisBundle(
        query=query, 
        articles=analyzed_articles, 
        summary_meta=_json_safe(summary_meta),
        patterns=patterns,
        topic_map=topic_map
    )
    bundle.insights = synthesize_insights(bundle.to_dict(), patterns)

    logger.info(f"✅ Processed {len(analyzed_articles)} articles with enhanced patterns.")
    return bundle


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyst Agent: Enhanced Topic Labeling & Pattern Analysis")
    parser.add_argument("--input", type=str, required=True, help="Path to researcher JSON output")
    parser.add_argument("--output", type=str, required=True, help="Path to save analysis JSON")
    parser.add_argument("--topic", type=str, default="", help="Optional topic name override")
    parser.add_argument("--yake", action="store_true", help="Use YAKE for keywords (requires yake package)")
    parser.add_argument("--force-cpu", action="store_true", help="Force CPU for NLTK/Spacy (not used but for CLI compatibility)")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    bundle = analyze_research_file(
        Path(args.input), 
        keyword_method="yake" if args.yake else "rake"
    )
    
    if args.topic:
        bundle.query = args.topic
        
    Path(args.output).write_text(json.dumps(bundle.to_dict(), indent=2), encoding="utf-8")
    print(f"Analysis saved to: {args.output}")


if __name__ == "__main__":
    main()
