# patterns.py
from collections import Counter, defaultdict
from datetime import datetime
import numpy as np

def detect_co_occurrences(articles, top_k=10):
    """Identify pairs of entities/keywords that frequently appear in the same article."""
    pair_counts = Counter()
    for art in articles:
        # Combine entities and keywords for a broader view
        terms = set(art.keywords)
        for label, entities in art.entities.items():
            terms.update([e.lower() for e in entities])
        
        # Sort terms to ensure (A, B) is same as (B, A)
        sorted_terms = sorted(list(terms))
        for i in range(len(sorted_terms)):
            for j in range(i + 1, len(sorted_terms)):
                pair_counts[(sorted_terms[i], sorted_terms[j])] += 1
                
    return [{"pair": list(pair), "count": count} for pair, count in pair_counts.most_common(top_k)]

def analyze_temporal_trends(articles):
    """Analyze article volume and average sentiment over time."""
    time_series = defaultdict(lambda: {"count": 0, "sentiment_sum": 0.0})
    
    for art in articles:
        date_str = art.published
        if not date_str:
            continue
            
        try:
            # Try parsing isoformat or just the date part
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            key = dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            # Fallback for other formats or if it's already just a date
            key = date_str[:10] if isinstance(date_str, str) else "Unknown"
            
        time_series[key]["count"] += 1
        time_series[key]["sentiment_sum"] += art.sentiment_score
        
    sorted_keys = sorted(time_series.keys())
    return [
        {
            "date": k,
            "count": time_series[k]["count"],
            "avg_sentiment": time_series[k]["sentiment_sum"] / time_series[k]["count"]
        }
        for k in sorted_keys
    ]

def find_divergent_entities(articles, min_mentions=3):
    """Identify entities that have polarizing sentiment across different sources."""
    entity_sentiments = defaultdict(list)
    for art in articles:
        for label, entities in art.entities.items():
            for ent in entities:
                entity_sentiments[ent.lower()].append(art.sentiment_score)
                
    divergence = []
    for ent, scores in entity_sentiments.items():
        if len(scores) >= min_mentions:
            variance = np.var(scores)
            if variance > 0.1: # Threshold for 'interesting' divergence
                divergence.append({
                    "entity": ent,
                    "variance": float(variance),
                    "mentions": len(scores),
                    "avg_sentiment": float(np.mean(scores))
                })
    return sorted(divergence, key=lambda x: x["variance"], reverse=True)[:5]

def calculate_historical_trend(articles):
    """Calculate a simple trend direction based on historical article dates."""
    trends = analyze_temporal_trends(articles)
    if len(trends) < 2:
        return {"direction": "stable", "growth_rate": 0.0, "data_points": len(trends)}
        
    # Simple linear slope logic
    counts = [t["count"] for t in trends]
    x = np.arange(len(counts))
    y = np.array(counts)
    slope, _ = np.polyfit(x, y, 1)
    
    direction = "upward" if slope > 0.1 else "downward" if slope < -0.1 else "stable"
    return {
        "direction": direction,
        "slope": float(slope),
        "data_points": len(trends),
        "recent_avg": float(np.mean(counts[-3:])) if len(counts) >=3 else float(np.mean(counts))
    }
