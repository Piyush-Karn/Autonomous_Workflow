from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any

@dataclass
class ArticleAnalysis:
    title: str
    url: str
    published: Optional[str]
    source: Optional[str]
    source_type: Optional[str]
    summary: str
    entities: Dict[str, List[str]]
    keywords: List[str]
    sentiment_score: float
    sentiment_label: str
    topic_cluster: Optional[int]
    source_weight: float
    extra: Optional[Dict[str, Any]]

@dataclass
class AnalysisBundle:
    query: str
    articles: List[ArticleAnalysis]
    summary_meta: Dict[str, Any]

    def to_dict(self):
        return asdict(self)
