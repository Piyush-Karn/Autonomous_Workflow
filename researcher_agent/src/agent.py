from .orchestrate import research
from .schema import ResearchBundle

def run_research(query: str, limit: int = 10, take: int = None) -> ResearchBundle:
    """
    Runs the full research workflow for the given query.
    limit = number of search results to fetch.
    take = number of articles to process (default: same as limit).
    """
    if take is None:
        take = limit
    return research(query, limit=limit, take_first_n=take)
