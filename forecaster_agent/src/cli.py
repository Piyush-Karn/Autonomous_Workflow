import argparse
import json
import logging
from pathlib import Path
from datetime import datetime
from . import forecaster

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="Run forecasting on Analyst Agent output JSON")
    parser.add_argument("input", type=Path, help="Analyst JSON file")
    parser.add_argument("--out", type=Path, help="Output file path (default: ./output/...)")
    parser.add_argument("--frequency", choices=["daily", "weekly"], default="daily")
    parser.add_argument("--horizon", type=int, default=14, help="Forecast horizon")
    parser.add_argument("--model", choices=["naive", "snaive", "holtwinters", "arima", "lightgbm", "xgboost"], default="snaive")
    parser.add_argument("--top-k-keywords", type=int, default=0, help="Include top-K keyword series")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if args.out is None:
        out_dir = Path("output")
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / f"forecast_{timestamp}.json"
    elif args.out.is_dir() or not args.out.suffix:
        args.out.mkdir(parents=True, exist_ok=True)
        out_path = args.out / f"forecast_{timestamp}.json"
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        stem, suffix = args.out.stem, args.out.suffix
        out_path = args.out.with_name(f"{stem}_{timestamp}{suffix}")

    result = forecaster.run_forecast(args.input, args.frequency, args.horizon, args.model, args.top_k_keywords)

    try:
        out_path.write_text(
            json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        logging.info(f"✅ Forecast saved: {out_path}")
    except Exception as e:
        logging.exception(f"❌ Failed to save forecast: {e}")


if __name__ == "__main__":
    main()
