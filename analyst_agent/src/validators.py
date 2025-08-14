# validators.py
def validate_article(article: dict) -> bool:
    """
    Basic validation for input articles from Researcher Agent.
    Checks mandatory keys and minimal text length.
    """
    if not isinstance(article, dict):
        return False
    required = ["title", "url", "text"]
    for key in required:
        if key not in article or not article[key]:
            return False
    # Require at least some length of text
    if len(article.get("text", "").strip()) < 50:
        return False
    return True
