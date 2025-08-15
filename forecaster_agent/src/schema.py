from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class SeriesForecast:
    series: str
    confidence: str
    forecasts: List[Dict[str, Any]]

@dataclass
class ForecastResult:
    meta: Dict[str, Any]
    forecasts: List[SeriesForecast]
    cv_metrics: Dict[str, Any]
    top_features: List[str]

    def to_dict(self):
        return {
            "meta": self.meta,
            "forecasts": [asdict(sf) for sf in self.forecasts],
            "cv_metrics": self.cv_metrics,
            "top_features": self.top_features
        }
