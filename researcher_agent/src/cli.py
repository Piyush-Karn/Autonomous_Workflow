import argparse
import json
from pathlib import Path
from datetime import datetime
from .agent import run_research

def main():
    parser = argparse.ArgumentParser(description="Researcher Agent CLI")
    parser.add_argument("query", help="Search query or topic")
    parser.add_argument(
        "--out",
        type=Path,
        help="Output JSON file (default: auto-generated with timestamp)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of search results to fetch (default: 10)"
    )
    parser.add_argument(
        "--take",
        type=int,
        help="Number of articles to process from fetched results (default: same as --limit)"
    )
    args = parser.parse_args()

    # Auto-generate filename if not provided
    if args.out is None:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_query = "_".join(args.query.lower().split())[:50]
        args.out = output_dir / f"research_output_{safe_query}_{timestamp}.json"

    bundle = run_research(args.query, limit=args.limit, take=args.take)
    args.out.write_text(
        json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"✅ Saved: {args.out}")

if __name__ == "__main__":
    main()
