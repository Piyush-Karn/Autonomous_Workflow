# Writer Agent

## Purpose
The Writer Agent converts Forecaster Agent outputs into **human-readable reports**.  
It is **topic-agnostic** — it works for market trend topics (e.g., *Electric Scooter Trends*) as well as investigative topics (e.g., *Scams in the Digital Marketspace*).

## Usage
```bash
python -m writer_agent.src.cli path/to/weekly_hw.json path/to/daily_snaive.json --out writer_agent/output/reports/report.html
