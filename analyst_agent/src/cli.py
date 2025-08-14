import argparse
import json
from pathlib import Path
from datetime import datetime
from .analyze import analyze_research_file

def main():
    parser = argparse.ArgumentParser(description="Analyst Agent CLI")
    parser.add_argument("input", type=Path, help="Research JSON file from Researcher Agent")
    parser.add_argument("--out", type=Path, help="Output file or folder for analysis JSON")
    args = parser.parse_args()

    print("📂 Loading research file...")
    if not args.input.exists():
        print(f"❌ Input file not found: {args.input}")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if args.out is None:
        # Default behavior: create output folder & timestamped file
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        args.out = output_dir / f"analysis_output_{timestamp}.json"
    else:
        # If output is a directory → save inside it with timestamp
        if args.out.is_dir() or not args.out.suffix:
            args.out.mkdir(parents=True, exist_ok=True)
            args.out = args.out / f"analysis_output_{timestamp}.json"
        else:
            # If output is a file path, insert timestamp before extension
            args.out.parent.mkdir(parents=True, exist_ok=True)
            stem = args.out.stem
            suffix = args.out.suffix
            args.out = args.out.with_name(f"{stem}_{timestamp}{suffix}")

    print("🧠 Extracting keywords and entities...")
    bundle = analyze_research_file(args.input)

    print("💾 Saving analysis...")
    args.out.write_text(
        json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"✅ Analysis saved: {args.out}")

if __name__ == "__main__":
    main()
