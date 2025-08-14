# Forecaster Agent

## Purpose
The Forecaster Agent Builds time-series datasets from Analyst outputs and predicts future trends.

## Usage
```bash
python -m forecaster_agent.src.cli
../analyst_agent/output/ai_in_education_2025-08-14_09-44-43.json
--horizon 14
--frequency daily
--model lightgbm
--out output/forecast.json
