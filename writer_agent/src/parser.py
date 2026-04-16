from datetime import datetime


def parse_all(raw, topic_override=None, mode="brief"):
    """
    Merge inputs (forecasts, analyst, facts) into a normalized structure for templates.
    """
    base = {
        "topic": topic_override or "Report",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mode": mode,
        "weekly": None,
        "daily": None,
        "summary": None,
        "analyst": None,
        "facts": None,
        "pro": None,
    }

    if "weekly" in raw:
        base["weekly"] = _parse_forecast(raw["weekly"])
    if "daily" in raw:
        base["daily"] = _parse_forecast(raw["daily"])

    base["summary"] = _build_executive_summary(base)

    if "analyst" in raw:
        base["analyst"] = _parse_analyst(raw["analyst"])
    if "facts" in raw:
        base["facts"] = _parse_facts(raw["facts"])

    if mode == "pro":
        base["pro"] = _build_pro_context(base)

    return base


def _parse_forecast(obj):
    meta = obj.get("meta", {})
    forecasts = obj.get("forecasts", []) or []

    # main series = article_count if present else first available
    main = next((f for f in forecasts if f.get("series") == "article_count"), forecasts[0] if forecasts else None)
    keywords = [f for f in forecasts if f.get("series") != "article_count"]

    return {
        "meta": meta,
        "main_series": main,
        "keyword_series": keywords,
        "cv_metrics": obj.get("cv_metrics", {}),
        "skipped_series": meta.get("skipped_series", []),
        "top_features": obj.get("top_features", []),
    }


def _parse_analyst(a):
    return {
        "summary_meta": a.get("summary_meta", {}),
        "articles": a.get("articles", []),
        "query": a.get("query", ""),
    }


def _parse_facts(f):
    return {
        "market_size_series": f.get("market_size_series"),
        "competitors": f.get("competitors"),
        "segments": f.get("segments"),
        "scam_incidents": f.get("scam_incidents"),
        "highlights": f.get("highlights"),
        "recommendations": f.get("recommendations"),
    }


def _build_executive_summary(parsed):
    """
    Executive summary:
    - Weekly: direction from first to last forecast value
    - Daily: unique value set to indicate seasonal-naive patterns
    """
    weekly = parsed.get("weekly")
    daily = parsed.get("daily")

    weekly_summary = None
    if weekly and weekly.get("main_series"):
        wf_list = (weekly["main_series"] or {}).get("forecasts") or []
        # Ensure list has at least one point with a 'prediction'
        if len(wf_list) >= 1:
            start_val = _safe_pred(wf_list, 0)
            end_val = _safe_pred(wf_list, len(wf_list) - 1)
            if end_val > start_val:
                direction = "upward"
            elif end_val < start_val:
                direction = "downward"
            else:
                direction = "flat"
            conf = weekly["main_series"].get("confidence") or weekly["meta"].get("confidence") or "N/A"
            weekly_summary = {
                "direction": direction,
                "start": round(start_val, 2),
                "end": round(end_val, 2),
                "horizon": weekly["meta"].get("horizon"),
                "confidence": conf,
            }

    daily_summary = None
    if daily and daily.get("main_series"):
        df_list = (daily["main_series"] or {}).get("forecasts") or []
        if df_list:
            unique_vals = sorted({round(_safe_pred(df_list, i), 2) for i in range(len(df_list))})
            conf = daily["main_series"].get("confidence") or daily["meta"].get("confidence") or "N/A"
            daily_summary = {
                "unique_values": unique_vals,
                "horizon": daily["meta"].get("horizon"),
                "confidence": conf,
            }

    return {"weekly": weekly_summary, "daily": daily_summary}


def _safe_pred(points, idx):
    """
    Safely extract a float prediction from points[idx] dict like {"date": "...", "prediction": ...}.
    """
    try:
        p = points[idx]
        return float(p.get("prediction", 0.0))
    except Exception:
        return 0.0


def _build_pro_context(parsed):
    analyst = parsed.get("analyst") or {}
    facts = parsed.get("facts") or {}
    return {
        "cover": {
            "title": parsed.get("topic"),
            "date": parsed.get("generated_at"),
            "prepared_by": "Multi-Agent Research Platform",
        },
        "exec": {
            "highlights": facts.get("highlights"),
            "weekly": parsed["summary"].get("weekly"),
            "daily": parsed["summary"].get("daily"),
            "top_entities": (analyst.get("summary_meta") or {}).get("top_entities"),
            "top_keywords": (analyst.get("summary_meta") or {}).get("top_keywords"),
        },
        "market_overview": {
            "market_size_series": facts.get("market_size_series"),
            "segments": facts.get("segments"),
        },
        "competitive": {
            "competitors": facts.get("competitors"),
        },
        "drivers_trends": {
            "top_keywords": (analyst.get("summary_meta") or {}).get("top_keywords"),
        },
        "forecast_analysis": {
            "weekly": parsed.get("weekly"),
            "daily": parsed.get("daily"),
            "market_size_series": facts.get("market_size_series"),
        },
        "recommendations": facts.get("recommendations"),
        "appendix": {
            "articles": analyst.get("articles"),
            "query": analyst.get("query"),
        },
    }
