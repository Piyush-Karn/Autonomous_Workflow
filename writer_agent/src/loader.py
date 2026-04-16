import json
from pathlib import Path


def load_inputs(weekly_path=None, daily_path=None, analyst_path=None, facts_path=None):
    out = {}
    if weekly_path:
        out["weekly"] = _load_json(weekly_path)
    if daily_path:
        out["daily"] = _load_json(daily_path)
    if analyst_path:
        out["analyst"] = _load_json(analyst_path)
    if facts_path:
        out["facts"] = _load_json(facts_path)
    if not out:
        raise ValueError("No inputs. Provide at least --weekly or --daily, optionally --analyst and --facts.")
    return out


def _load_json(p: Path):
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
