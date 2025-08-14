import argparse
import json
from pathlib import Path
from datetime import datetime
from .analyze import analyze_research_file

def main():
    parser = argparse.ArgumentParser(description="Analyst Agent CLI")
    parser.add_argument("input", type=Path, help="Research JSON file from Researcher Agent")
    parser.add_argument("--out", type=Path, help="Output analysis JSON file")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"❌ Input file not found: {args.input}")
        return

    if args.out is None:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        args.out = output_dir / f"analysis_output_{timestamp}.json"

    bundle = analyze_research_file(args.input)
    args.out.write_text(json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Analysis saved: {args.out}")

if __name__ == "__main__":
    main()
