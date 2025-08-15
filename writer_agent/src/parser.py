from datetime import datetime


def parse_forecast_data(raw_data, topic_override=None):
    """
    Convert loaded JSONs into a normalized structure for templates.
    """
    parsed = {
        "topic": topic_override or _infer_topic(raw_data),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "weekly": None,
        "daily": None,
        "summary": None,
    }

    if "weekly" in raw_data:
        parsed["weekly"] = _parse_single_forecast(raw_data["weekly"])
    if "daily" in raw_data:
        parsed["daily"] = _parse_single_forecast(raw_data["daily"])

    parsed["summary"] = _build_executive_summary(parsed)
    return parsed


def _parse_single_forecast(json_obj):
    meta = json_obj.get("meta", {})
    forecasts = json_obj.get("forecasts", [])

    # Detect main series as article_count if present, else fallback to first series
    main_series = next((f for f in forecasts if f.get("series") == "article_count"), None)
    if not main_series and forecasts:
        main_series = forecasts[0]

    keyword_series = [f for f in forecasts if f.get("series") != "article_count"]

    return {
        "meta": meta,
        "main_series": main_series,
        "keyword_series": keyword_series,
        "cv_metrics": json_obj.get("cv_metrics", {}),
        "skipped_series": meta.get("skipped_series", []),
        "top_features": json_obj.get("top_features", []),
    }


def _infer_topic(raw_data):
    # If no explicit topic, return a generic label
    return "Forecast Report"


def _build_executive_summary(parsed):
    """
    Build a lightweight executive summary:
    - Weekly: direction and magnitude from first to last point
    - Daily: note on unique values (e.g., seasonal naive repeating pattern)
    """
    weekly = parsed.get("weekly")
    daily = parsed.get("daily")

    weekly_summary = None
    if weekly and weekly.get("main_series") and weekly["main_series"].get("forecasts"):
        wf = weekly["main_series"]["forecasts"]
        start_val = wf[0]["prediction"]
        end_val = wf[-1]["prediction"]
        direction = "upward" if end_val > start_val else ("downward" if end_val < start_val else "flat")
        conf = weekly["main_series"].get("confidence") or weekly["meta"].get("confidence") or "N/A"
        weekly_summary = {
            "direction": direction,
            "start": round(float(start_val), 2),
            "end": round(float(end_val), 2),
            "horizon": weekly["meta"].get("horizon"),
            "confidence": conf,
        }

    daily_summary = None
    if daily and daily.get("main_series") and daily["main_series"].get("forecasts"):
        dfc = daily["main_series"]["forecasts"]
        unique_vals = sorted({round(float(p["prediction"]), 2) for p in dfc})
        conf = daily["main_series"].get("confidence") or daily["meta"].get("confidence") or "N/A"
        daily_summary = {
            "unique_values": unique_vals,
            "horizon": daily["meta"].get("horizon"),
            "confidence": conf,
        }

    return {"weekly": weekly_summary, "daily": daily_summary}
