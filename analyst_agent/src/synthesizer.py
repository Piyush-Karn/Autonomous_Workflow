# synthesizer.py

def synthesize_insights(bundle_data, patterns):
    """
    Generate a high-quality narrative summary of the analysis findings.
    """
    query = bundle_data.get("query", "the subject")
    total_articles = bundle_data.get("summary_meta", {}).get("total_articles", 0)
    avg_sentiment = bundle_data.get("summary_meta", {}).get("avg_sentiment", 0)
    top_entities = bundle_data.get("summary_meta", {}).get("top_entities", [])
    
    # 1. Title/Overview
    sent_desc = "bullish/positive" if avg_sentiment > 0.2 else "bearish/critical" if avg_sentiment < -0.2 else "balanced"
    overview = f"The current discourse surrounding '{query}' across {total_articles} analyzed sources is overall {sent_desc}."

    # 2. Executive Highlights (Categorized)
    highlights = []
    
    # Entity/Focus Analysis
    # Filter out common placeholders from top entities
    IGNORE_ENTITIES = {"india", "indian", "two", "ev", "electrical"}
    significant_entities = [e[0] for e in top_entities if e[0].lower() not in IGNORE_ENTITIES][:4]
    if significant_entities:
        highlights.append(f"**Dominant Themes**: Industry attention is primarily focused on {', '.join(significant_entities)}.")

    # Patterns: Co-occurrence (Consensus)
    co_oc = patterns.get("co_occurrences", [])
    if co_oc:
        strongest = co_oc[0]
        highlights.append(f"**Strategic Linkages**: A notable correlation exists between **{strongest['pair'][0].capitalize()}** and **{strongest['pair'][1].capitalize()}**, suggesting these concepts are inextricably linked in recent coverage.")

    # Patterns: Divergence (Conflict/Complexity)
    div = patterns.get("divergent_entities", [])
    if div:
        polarizing = [d["entity"].capitalize() for d in div[:2]]
        highlights.append(f"**Points of Divergence**: Analytical consensus is least stable regarding **{', '.join(polarizing)}**, where sentiment varies significantly across different reporting outlets.")

    # 3. Temporal Context
    trends = patterns.get("temporal_trends", [])
    trend_note = ""
    if len(trends) > 1:
        first, last = trends[0], trends[-1]
        growth = "accelerating" if last["count"] > first["count"] else "consolidating" if last["count"] < first["count"] else "steady"
        trend_note = f"\n\nFrom a temporal perspective, the volume of reporting is **{growth}**, indicating { 'rising' if growth == 'accelerating' else 'stable' } market interest."

    # Final Assembly
    full_narrative = [
        overview,
        "### 💡 Executive Highlights",
        "\n".join([f"- {h}" for h in highlights]),
        trend_note
    ]

    return "\n\n".join(full_narrative)
