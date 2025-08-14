# cli.py
import argparse
import json
from pathlib import Path
from . import forecaster, config, utils

def main():
    utils.setup_logger()
    parser = argparse.ArgumentParser(description="Run Forecaster Agent")
    parser.add_argument("input", type=Path, help="Analyst Agent JSON file")
    parser.add_argument("--horizon", type=int, default=config.DEFAULT_HORIZON, help="Forecast horizon length")
    parser.add_argument("--frequency", choices=["daily","weekly"], default=config.DEFAULT_FREQUENCY, help="Time series frequency")
    parser.add_argument("--model", choices=["naive","snaive","holtwinters","arima","lightgbm","xgboost"], default=config.DEFAULT_MODEL, help="Forecast model type")
    parser.add_argument("--top-k-keywords", type=int, default=config.DEFAULT_TOP_K_KEYWORDS, help="Include counts of top-K keywords as features (0 to disable)")
    parser.add_argument("--out", type=Path, help="Output forecast JSON file")
    args = parser.parse_args()

    result = forecaster.run_forecast(args.input, args.frequency, args.horizon, args.model, args.top_k_keywords)

    if args.out is None:
        out_path = Path("output") / f"forecast_{utils.timestamp()}.json"
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        out_path = args.out
    out_path.write_text(json.dumps(result.__dict__, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Forecast saved: {out_path}")

if __name__ == "__main__":
    main()

