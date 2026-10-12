# Google Stock Agent

A simple agent that fetches a daily summary of Google (GOOGL) stock and commits it to this repo each weekday morning.

## How it works

- GitHub Actions runs the script every weekday at **9:00 AM UTC**
- The script pulls live data from Yahoo Finance via `yfinance`
- A Markdown summary is saved to `summaries/YYYY-MM-DD.md` and `summaries/latest.md`
- The workflow automatically commits and pushes the new file

## Latest summary

See [summaries/latest.md](summaries/latest.md) for the most recent report.

## Run locally

```bash
pip install -r requirements.txt
python stock_agent.py
```

## Manual trigger

Go to **Actions → Daily Google Stock Summary → Run workflow** to trigger a run on demand.
