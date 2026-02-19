import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gsp_core import (
    DEFAULT_DATA_PATH,
    actor_rollups,
    ensure_genesis,
    load_entries,
    record_event,
    reconstruct_timeline,
    verify_file,
)


def _parse_payload(raw: str | None) -> dict:
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON payload: {exc}") from exc


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Glass Substrate demo terminal app")
    parser.add_argument(
        "--path",
        default=str(DEFAULT_DATA_PATH),
        help="Path to JSON event log (default: data/sample_events.json)",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="Create genesis record if missing")

    append_cmd = sub.add_parser("append", help="Append a new event")
    append_cmd.add_argument("--actor", required=True)
    append_cmd.add_argument("--action", required=True)
    append_cmd.add_argument("--payload", help="JSON payload string", default="{}")

    sub.add_parser("verify", help="Verify hash chain integrity")
    sub.add_parser("show", help="Display stored events and summary (default)")

    args = parser.parse_args(argv)
    log_path = args.path

    if args.command in (None, "show"):
        entries = ensure_genesis(log_path)
        timeline = reconstruct_timeline(entries)
        print(json.dumps(timeline, indent=2))
        print("Actor rollup:", actor_rollups(entries))
        return

    if args.command == "init":
        ensure_genesis(log_path)
        print(f"Initialized log at {log_path}")
        return

    if args.command == "append":
        payload = _parse_payload(args.payload)
        event = record_event(args.actor, args.action, payload, path=log_path)
        print(json.dumps(event, indent=2))
        return

    if args.command == "verify":
        result = verify_file(log_path)
        print(json.dumps(result, indent=2))
        return


if __name__ == "__main__":
    main()
