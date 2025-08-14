# schema.py
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TimeSeries:
    dates: List[str]  # ISO date strings
    values: List[float]  # numerical target values
    features: Dict[str, List[float]]  # optional exogenous features

@dataclass
class ForecastResult:
    meta: Dict[str, Any]
    forecasts: List[Dict[str, Any]]
    cv_metrics: Dict[str, float]
    top_features: List[Dict[str, Any]]
