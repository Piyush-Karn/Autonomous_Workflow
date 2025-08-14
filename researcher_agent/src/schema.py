from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class Article:
    title: Optional[str]
    url: str
    authors: List[str]
    published: Optional[str]          # standardized date string
    top_image: Optional[str]
    summary: Optional[str]
    text: str
    source: Optional[str]
    source_type: Optional[str]        # NEW FIELD
    word_count: int
    status: str
    error: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

    def to_dict(self):
        d = asdict(self)
        d["retrieved_at"] = datetime.now(timezone.utc).isoformat()
        return d

@dataclass
class ResearchBundle:
    query: str
    articles: List[Article]

    def to_dict(self):
        return {
            "query": self.query,
            "articles": [a.to_dict() for a in self.articles]
        }
