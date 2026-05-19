from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ga_multica import MulticaClient, dispatch_issue
from ga_multica.ceo import DEFAULT_REGISTRY_PATH, read_text_input


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and assign a Multica issue for a CEO task.")
    parser.add_argument("--title", required=True, help="Issue title.")
    parser.add_argument("--worker", required=True, help="Worker name or agent_id from workspace/worker_registry.json.")
    parser.add_argument("--description", help="Inline issue description text.")
    parser.add_argument("--description-file", help="Read issue description from a UTF-8 file.")
    parser.add_argument("--description-stdin", action="store_true", help="Read issue description from stdin.")
    parser.add_argument("--priority", default="high", help="Issue priority.")
    parser.add_argument("--status", default="todo", help="Initial issue status.")
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_REGISTRY_PATH),
        help="Path to worker_registry.json.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    description = read_text_input(
        text=args.description,
        file_path=args.description_file,
        use_stdin=args.description_stdin,
    )
    client = MulticaClient()
    result = dispatch_issue(
        client,
        title=args.title,
        description=description,
        worker_ref=args.worker,
        registry_path=args.registry,
        priority=args.priority,
        status=args.status,
    )
    print(json.dumps({"id": result.get("id"), "identifier": result.get("identifier")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
