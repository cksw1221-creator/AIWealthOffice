from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ga_multica import MulticaClient, review_issue
from ga_multica.ceo import read_text_input


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Request rework on a Multica issue and keep it actionable.")
    parser.add_argument("issue", help="Issue ID or key.")
    parser.add_argument("--comment", help="Inline CEO rework comment.")
    parser.add_argument("--comment-file", help="Read CEO rework comment from a UTF-8 file.")
    parser.add_argument("--comment-stdin", action="store_true", help="Read CEO rework comment from stdin.")
    parser.add_argument("--status", default="todo", help="Status to set after rework request.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    comment = read_text_input(
        text=args.comment,
        file_path=args.comment_file,
        use_stdin=args.comment_stdin,
    )
    result = review_issue(MulticaClient(), issue_id=args.issue, comment=comment, status=args.status)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
