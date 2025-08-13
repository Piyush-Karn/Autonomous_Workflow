import json
import argparse
from pathlib import Path
from .orchestrate import research

def main():
    p = argparse.ArgumentParser(description="Researcher Agent")
    p.add_argument("query", type=str, help="Topic or question to research")
    p.add_argument("--max_results", type=int, default=8)
    p.add_argument("--take", type=int, default=6)
    p.add_argument("--out", type=Path, default=Path("research_output.json"))
    args = p.parse_args()

    bundle = research(args.query, args.max_results, args.take)
    args.out.write_text(json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2))
    print(f"✅ Saved: {args.out.resolve()}")

if __name__ == "__main__":
    main()
