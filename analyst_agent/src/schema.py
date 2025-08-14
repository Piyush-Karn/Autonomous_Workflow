from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class ArticleAnalysis:
    title: str
    url: str
    summary: str
    entities: Dict[str, List[str]]
    keywords: List[str]

@dataclass
class AnalysisBundle:
    query: str
    articles: List[ArticleAnalysis]

    def to_dict(self):
        return asdict(self)
