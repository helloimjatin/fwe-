import random

HOOKS = [
    "This week in AI:",
    "AI roundup you can skim in 30 seconds:",
    "What’s new in the AI world:",
    "AI updates worth your coffee:",
]

EMOJIS = ["✨", "🚀", "🧠", "🛠️", "📚", "📝", "🔍", "📢"]


def make_bullets(items, n, include_emojis=True):
    out = []
    for i, it in enumerate(items[:n]):
        emoji = (EMOJIS[i % len(EMOJIS)] + " ") if include_emojis else ""
        title = it['title'].strip().rstrip('.')
        link = it['link']
        summary = it.get('short', '').strip()
        # Keep bullets tight for LinkedIn; avoid raw URLs if you prefer
        if summary:
            out.append(f"• {emoji}{title} — {summary} ({link})")
        else:
            out.append(f"• {emoji}{title} ({link})")
    return "\n".join(out)


def compose_post(items, hashtags, cta, bullets=5, include_emojis=True):
    hook = random.choice(HOOKS)
    body = make_bullets(items, bullets, include_emojis)
    tags = " ".join(hashtags)
    return f"{hook}\n\n{body}\n\n{cta}\n\n{tags}"
