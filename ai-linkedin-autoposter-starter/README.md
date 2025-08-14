# AI LinkedIn Autoposter (Free & Compliant) – Starter Repo

This repo generates an AI news/tools digest twice a week using free sources (RSS), summarizes items, composes a LinkedIn-ready post, and saves it in `out/` (plus optional Telegram delivery).

## Quick Start
1) Add/adjust `config.yaml` (feeds, hashtags, bullets).  
2) (Optional) Add GitHub Actions secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.  
3) Push the repo. The workflow runs Mon & Thu 09:00 IST (03:30 UTC).  
4) Or run manually from the **Actions** tab with **Run workflow**.  
5) Find the generated post in `out/LinkedIn_Post_YYYY-MM-DD.md`.

## Local Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
. .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Notes
- Safe & compliant: no unofficial LinkedIn posting.
- Customize tone in `src/compose.py` and hashtags/CTA in `config.yaml`.
