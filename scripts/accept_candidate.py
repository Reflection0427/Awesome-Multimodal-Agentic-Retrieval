#!/usr/bin/env python3
"""Move one reviewed candidate into the curated paper list."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "data" / "papers.json"
CANDIDATES = ROOT / "data" / "candidates.json"


def slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value[:70].rstrip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description="Accept a human-reviewed paper candidate")
    parser.add_argument("query", help="unique title substring")
    parser.add_argument("--section", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--framework", action="append", required=True, help="repeat 3-5 times")
    parser.add_argument("--code-url", default="")
    args = parser.parse_args()
    if not 3 <= len(args.framework) <= 5:
        parser.error("--framework must be supplied 3-5 times")
    papers = json.loads(PAPERS.read_text(encoding="utf-8"))
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    matches = [row for row in candidates if args.query.lower() in row["title"].lower()]
    if len(matches) != 1:
        parser.error(f"expected exactly one match, found {len(matches)}")
    candidate = matches[0]
    year_match = re.search(r"20\d{2}", candidate.get("published", ""))
    paper = {
        "id": slug(candidate["title"]),
        "title": candidate["title"],
        "year": int(year_match.group()) if year_match else 0,
        "venue": candidate.get("venue") or "To appear",
        "paper_url": candidate["paper_url"],
        "code_url": args.code_url,
        "section": args.section,
        "summary": args.summary,
        "framework": args.framework,
    }
    papers.append(paper)
    candidates.remove(candidate)
    PAPERS.write_text(json.dumps(papers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CANDIDATES.write_text(json.dumps(candidates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_readme.py")], check=True)
    print(f"Accepted: {paper['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
