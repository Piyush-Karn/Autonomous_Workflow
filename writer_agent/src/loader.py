import json
from pathlib import Path


def load_forecasts(weekly_path=None, daily_path=None):
    """
    Load weekly and daily forecast JSON files from Forecaster Agent.
    """
    output = {}
    if weekly_path:
        output["weekly"] = _load_json_file(weekly_path)
    if daily_path:
        output["daily"] = _load_json_file(daily_path)

    if not output:
        raise ValueError("No forecast JSONs provided. Pass --weekly and/or --daily.")
    return output


def _load_json_file(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Forecast file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Basic schema check
    if "forecasts" not in data or "meta" not in data:
        raise ValueError(f"Invalid forecast file structure: {path}")
    return data
