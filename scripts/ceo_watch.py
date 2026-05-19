from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ga_multica import MulticaClient, format_issue_summary, poll_issue


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize the latest Multica issue execution state.")
    parser.add_argument("issue", help="Issue ID or key.")
    parser.add_argument("--since-seq", type=int, help="Only fetch run messages after this sequence number.")
    parser.add_argument("--json", action="store_true", help="Print raw JSON summary.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = poll_issue(MulticaClient(), args.issue, since_seq=args.since_seq)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(format_issue_summary(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
