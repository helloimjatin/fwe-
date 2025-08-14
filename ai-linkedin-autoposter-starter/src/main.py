import os
import json
import yaml
import pathlib
from datetime import datetime
from typing import Dict, List
import requests

from sources import fetch_feed
from fetch_and_rank import rank_items
from summarize import summarize

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "out"
STATE = DATA / "state.json"


def load_cfg() -> Dict:
    with open(ROOT / "config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_state() -> Dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"seen": []}


def save_state(state: Dict):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def notify_telegram(text: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text}
        )
    except Exception as e:
        print("Telegram notify failed:", e)


def main():
    cfg = load_cfg()
    state = load_state()

    # 1) Fetch
    raw_items: List[Dict] = []
    for src in cfg["feeds"]:
        try:
            items = fetch_feed(src["url"])[: cfg.get("max_items_per_source", 5)]
            raw_items.extend(items)
        except Exception as e:
            print("Feed error", src, e)

    # 2) Dedup by link/id
    seen = set(state.get("seen", []))
    uniq = []
    for it in raw_items:
        uid = it.get("id") or it.get("link")
        if uid and uid not in seen:
            uniq.append(it)
    # cap total
    uniq = uniq[: cfg.get("max_total_items", 25)]

    # 3) Rank
    ranked = rank_items(uniq, cfg)

    # 4) Summarize top N to enrich bullets
    top_for_bullets = ranked[: max(5, cfg["post"]["bullets"])]
    for it in top_for_bullets:
        it["short"] = summarize(it.get("summary", ""), sentences=cfg["summary"]["sentences"]).strip()

    # 5) Compose
    from compose import compose_post
    post_text = compose_post(
        top_for_bullets,
        cfg["post"]["hashtags"],
        cfg["post"]["cta"],
        bullets=cfg["post"]["bullets"],
        include_emojis=cfg["post"].get("include_emojis", True)
    )

    # 6) Persist output
    OUT.mkdir(parents=True, exist_ok=True)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    out_path = OUT / f"LinkedIn_Post_{today}.md"
    out_path.write_text(post_text, encoding="utf-8")

    # 7) Update state (mark as seen)
    all_seen = list(seen) + [it.get("id") or it.get("link") for it in top_for_bullets]
    state["seen"] = all_seen[-5000:]  # keep last 5k
    save_state(state)

    # 8) Notify
    notify_telegram(f"✅ AI digest ready: {out_path.name}\n\n" + post_text[:3500])

    print("Done.")


if __name__ == "__main__":
    main()
