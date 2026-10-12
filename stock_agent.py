#!/usr/bin/env python3
"""Daily Google stock summary agent."""

import yfinance as yf
from datetime import datetime, timedelta
import os

TICKER = "GOOGL"


def fetch_stock_data():
    stock = yf.Ticker(TICKER)
    info = stock.info
    hist = stock.history(period="5d")
    return info, hist


def build_summary(info, hist):
    today = datetime.now().strftime("%Y-%m-%d")

    current_price = info.get("currentPrice") or info.get("regularMarketPrice", "N/A")
    prev_close = info.get("previousClose", "N/A")
    day_high = info.get("dayHigh") or info.get("regularMarketDayHigh", "N/A")
    day_low = info.get("dayLow") or info.get("regularMarketDayLow", "N/A")
    market_cap = info.get("marketCap", "N/A")
    volume = info.get("volume") or info.get("regularMarketVolume", "N/A")
    pe_ratio = info.get("trailingPE", "N/A")
    week_52_high = info.get("fiftyTwoWeekHigh", "N/A")
    week_52_low = info.get("fiftyTwoWeekLow", "N/A")

    # Calculate daily change
    change = "N/A"
    change_pct = "N/A"
    if isinstance(current_price, (int, float)) and isinstance(prev_close, (int, float)):
        change = current_price - prev_close
        change_pct = (change / prev_close) * 100
        change_str = f"{'▲' if change >= 0 else '▼'} ${abs(change):.2f} ({change_pct:+.2f}%)"
    else:
        change_str = "N/A"

    def fmt_price(v):
        return f"${v:.2f}" if isinstance(v, (int, float)) else str(v)

    def fmt_large(v):
        if isinstance(v, (int, float)):
            if v >= 1e12:
                return f"${v / 1e12:.2f}T"
            if v >= 1e9:
                return f"${v / 1e9:.2f}B"
            if v >= 1e6:
                return f"${v / 1e6:.2f}M"
        return str(v)

    def fmt_vol(v):
        if isinstance(v, (int, float)):
            return f"{int(v):,}"
        return str(v)

    # 5-day history table
    history_rows = ""
    if not hist.empty:
        for date, row in hist.tail(5).iterrows():
            d = date.strftime("%Y-%m-%d")
            o = f"${row['Open']:.2f}"
            h = f"${row['High']:.2f}"
            l = f"${row['Low']:.2f}"
            c = f"${row['Close']:.2f}"
            v = f"{int(row['Volume']):,}"
            history_rows += f"| {d} | {o} | {h} | {l} | {c} | {v} |\n"

    summary = f"""# Google (GOOGL) Stock Summary — {today}

## Current Snapshot

| Metric | Value |
|---|---|
| Current Price | {fmt_price(current_price)} |
| Previous Close | {fmt_price(prev_close)} |
| Daily Change | {change_str} |
| Day High | {fmt_price(day_high)} |
| Day Low | {fmt_price(day_low)} |
| Volume | {fmt_vol(volume)} |
| Market Cap | {fmt_large(market_cap)} |
| P/E Ratio | {pe_ratio if pe_ratio == 'N/A' else f'{pe_ratio:.2f}'} |
| 52-Week High | {fmt_price(week_52_high)} |
| 52-Week Low | {fmt_price(week_52_low)} |

## 5-Day Price History

| Date | Open | High | Low | Close | Volume |
|---|---|---|---|---|---|
{history_rows.strip()}

---
*Generated on {datetime.now().strftime("%Y-%m-%d at %H:%M UTC")}*
"""
    return summary, today


def save_summary(summary, today):
    os.makedirs("summaries", exist_ok=True)
    filepath = f"summaries/{today}.md"
    with open(filepath, "w") as f:
        f.write(summary)
    # Keep a latest.md for easy access
    with open("summaries/latest.md", "w") as f:
        f.write(summary)
    print(f"Summary saved to {filepath}")
    return filepath


if __name__ == "__main__":
    print(f"Fetching {TICKER} stock data...")
    info, hist = fetch_stock_data()
    summary, today = build_summary(info, hist)
    print(summary)
    save_summary(summary, today)
