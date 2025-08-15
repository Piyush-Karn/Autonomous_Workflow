import argparse
from pathlib import Path

from . import loader, parser, generator


def main():
    parser_cli = argparse.ArgumentParser(
        description="Writer Agent: Generate narrative reports from Forecaster JSONs."
    )
    parser_cli.add_argument(
        "--weekly", type=Path, required=False, help="Path to weekly forecast JSON"
    )
    parser_cli.add_argument(
        "--daily", type=Path, required=False, help="Path to daily forecast JSON"
    )
    parser_cli.add_argument(
        "--out", type=Path, required=True, help="Output file path (.md, .html, .pdf)"
    )
    parser_cli.add_argument(
        "--topic-name", type=str, default=None, help="Override topic name in report"
    )
    parser_cli.add_argument(
        "--skip-charts", action="store_true", help="Disable chart generation"
    )
    args = parser_cli.parse_args()

    # Load forecast JSONs
    data = loader.load_forecasts(weekly_path=args.weekly, daily_path=args.daily)

    # Parse into structured form
    parsed = parser.parse_forecast_data(data, topic_override=args.topic_name)

    # Generate report
    generator.generate_report(parsed, out_path=args.out, skip_charts=args.skip_charts)


if __name__ == "__main__":
    main()
