from __future__ import annotations

import argparse
import sys

from interfaces.terminal_app import main as terminal_main


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Glass Substrate demo entrypoint")
    parser.add_argument(
        "--web",
        action="store_true",
        help="Start the lightweight web dashboard instead of the terminal app",
    )
    parser.add_argument(
        "--storage",
        help="Optional path to the storage.json file",
        default=None,
    )
    args, remainder = parser.parse_known_args(argv)
    args.remainder = remainder
    return args


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.web:
        from interfaces.web_dashboard import create_app

        app = create_app(storage_path=args.storage)
        app.run(host="0.0.0.0", port=5055, debug=True)
        return

    forwarded = args.remainder
    if args.storage:
        forwarded = ["--storage", args.storage, *forwarded]
    terminal_main(forwarded)


if __name__ == "__main__":
    main(sys.argv[1:])
import json
from pathlib import Path

from gsp_core import (
    DEFAULT_DATA_PATH,
    actor_rollups,
    ensure_genesis,
    load_entries,
    record_event,
    reconstruct_timeline,
    verify_file,
)


def main() -> None:
    log_path = Path(DEFAULT_DATA_PATH)
    ensure_genesis(log_path)

    sample_event = record_event(
        actor="demo-runner",
        action="sample-attestation",
        payload={"context": "main.py", "path": str(log_path)},
        path=str(log_path),
    )

    verification = verify_file(str(log_path))
    timeline = reconstruct_timeline(load_entries(str(log_path)))

    print("Wrote event:")
    print(json.dumps(sample_event, indent=2))
    print("\nVerification:")
    print(json.dumps(verification, indent=2))
    print("\nActor rollup:")
    print(actor_rollups(load_entries(str(log_path))))
    print("\nTimeline (truncated):")
    print(json.dumps(timeline["timeline"][:3], indent=2))


if __name__ == "__main__":
    main()
