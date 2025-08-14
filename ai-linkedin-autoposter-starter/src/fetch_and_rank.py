import re
from typing import List, Dict, Tuple
from datetime import datetime
from dateutil import parser as dtparser


def _score(item: Dict, must_any, boost, drop_if_any) -> float:
    text = f"{item['title']}\n{item['summary']}".lower()
    if any(bad.lower() in text for bad in drop_if_any):
        return -1e9
    base = 0.0
    if must_any:
        if not any(k.lower() in text for k in must_any):
            base -= 1.0
    for b in boost:
        if b.lower() in text:
            base += 0.5
    # recency bonus (days ago → score)
    try:
        dt = dtparser.parse(item.get("published") or "")
        days = max((datetime.utcnow() - dt.replace(tzinfo=None)).days, 0)
        base += max(0, 7 - days) * 0.1
    except Exception:
        pass
    # title length sanity
    tlen = len(item.get("title", ""))
    if 10 <= tlen <= 140:
        base += 0.2
    return base


def rank_items(items: List[Dict], cfg: Dict) -> List[Dict]:
    scored = []
    for it in items:
        s = _score(it, cfg["keywords"].get("must_any", []), cfg["keywords"].get("boost", []), cfg["keywords"].get("drop_if_any", []))
        if s > -1e8:
            scored.append((s, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [it for _, it in scored]
