import requests
from requests.exceptions import RequestException, Timeout

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ResearcherAgent/1.0)"
}

def fetch_url(url: str, timeout: int = 12):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if "text/html" not in r.headers.get("Content-Type", ""):
            return None, "Non-HTML content"
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}"
        return r.text, None
    except (RequestException, Timeout) as e:
        return None, str(e)
