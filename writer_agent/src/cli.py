import argparse
from pathlib import Path

from . import loader, parser, generator


def main():
    parser_cli = argparse.ArgumentParser(
        description="Writer Agent: Generate reports (brief/pro) from Forecaster/Analyst JSONs."
    )
    parser_cli.add_argument("--weekly", type=Path, required=False, help="Path to weekly forecast JSON")
    parser_cli.add_argument("--daily", type=Path, required=False, help="Path to daily forecast JSON")
    parser_cli.add_argument("--analyst", type=Path, required=False, help="Path to Analyst JSON (articles, meta)")
    parser_cli.add_argument("--facts", type=Path, required=False, help="Path to curated facts JSON (market size, competitors, incidents)")
    parser_cli.add_argument("--out", type=Path, required=True, help="Output file (.md/.html/.pdf)")
    parser_cli.add_argument("--topic-name", type=str, default=None, help="Override topic name")
    parser_cli.add_argument("--skip-charts", action="store_true", help="Disable chart generation")
    parser_cli.add_argument("--mode", type=str, choices=["brief", "pro"], default="brief", help="Report mode: brief or pro")
    args = parser_cli.parse_args()

    data = loader.load_inputs(weekly_path=args.weekly, daily_path=args.daily, analyst_path=args.analyst, facts_path=args.facts)
    parsed = parser.parse_all(data, topic_override=args.topic_name, mode=args.mode)
    generator.generate_report(parsed, out_path=args.out, skip_charts=args.skip_charts)


if __name__ == "__main__":
    main()
