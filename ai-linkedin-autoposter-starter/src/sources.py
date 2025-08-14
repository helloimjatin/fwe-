import feedparser
from typing import List, Dict

def fetch_feed(url: str) -> List[Dict]:
    feed = feedparser.parse(url)
    items = []
    for e in feed.entries:
        items.append({
            "title": e.get("title", "").strip(),
            "link": e.get("link", "").strip(),
            "summary": (e.get("summary") or e.get("description") or "").strip(),
            "published": e.get("published") or e.get("updated") or "",
            "id": e.get("id") or e.get("link")
        })
    return items
