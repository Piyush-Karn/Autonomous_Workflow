# cli.py
import argparse
import json
import logging
from .analyze import _json_safe 
from pathlib import Path
from datetime import datetime

from .analyze import analyze_research_file

# Set up logging
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Run Analyst Agent on a research JSON file")
    parser.add_argument(
        "input",
        type=Path,
        help="Path to research JSON file from Researcher Agent"
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Output file or folder for analysis JSON (default: ./output/...)"
    )
    parser.add_argument(
        "--keywords",
        choices=["rake", "yake"],
        default="rake",
        help="Keyword extraction method to use (default: rake)"
    )

    args = parser.parse_args()
    logging.info("📂 Loading research file...")

    if not args.input.exists() or not args.input.is_file():
        logging.error(f"❌ Input file not found or not a file: {args.input}")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Determine output path
    if args.out is None:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        out_path = output_dir / f"analysis_output_{timestamp}.json"
    elif args.out.is_dir() or not args.out.suffix:
        # Directory or no extension - treat as folder
        args.out.mkdir(parents=True, exist_ok=True)
        out_path = args.out / f"analysis_output_{timestamp}.json"
    else:
        # File path given — append timestamp before extension
        args.out.parent.mkdir(parents=True, exist_ok=True)
        stem, suffix = args.out.stem, args.out.suffix
        out_path = args.out.with_name(f"{stem}_{timestamp}{suffix}")

    logging.info(f"🧠 Analyzing with '{args.keywords}' keyword method...")
    try:
        bundle = analyze_research_file(args.input, keyword_method=args.keywords)
    except Exception as e:
        logging.exception(f"❌ Analysis failed: {e}")
        return

    logging.info("💾 Saving analysis...")
    try:
        
        safe_bundle = _json_safe(bundle.to_dict())
        out_path.write_text(
            json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception as e:
        logging.exception(f"❌ Failed to save analysis to {out_path}: {e}")
        return

    logging.info(f"✅ Analysis saved: {out_path}")

if __name__ == "__main__":
    main()


