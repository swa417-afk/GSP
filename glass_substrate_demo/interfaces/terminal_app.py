from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from gsp_core import Engine, Storage, Verification
from gsp_core.reconstruction import Reconstruction
from visualizations.charts import ascii_bar, policy_counts


def _engine(storage_path: str | None = None) -> Engine:
    storage = Storage(Path(storage_path) if storage_path else None)
    verifier = Verification()
    return Engine(storage=storage, verifier=verifier)


def _print_records(records: List[dict]) -> None:
    if not records:
        print("No records found.")
        return

    headers = ["id", "model", "policy", "actor", "timestamp", "hash"]
    print(" | ".join(headers))
    print("-" * 80)
    for record in records:
        print(
            " | ".join(
                [
                    record.get("record_id", "")[:8],
                    record.get("model_id", ""),
                    record.get("policy_id", ""),
                    record.get("actor", ""),
                    record.get("timestamp", ""),
                    (record.get("record_hash", "") or "")[:12],
                ]
            )
        )


def cmd_list(args: argparse.Namespace) -> None:
    engine = _engine(args.storage)
    _print_records(engine.list_records())


def cmd_add(args: argparse.Namespace) -> None:
    engine = _engine(args.storage)
    record = engine.submit(
        model_id=args.model,
        input_hash=args.input_hash,
        output_hash=args.output_hash,
        policy_id=args.policy,
        actor=args.actor,
        notes=args.notes,
    )
    print("Added record:")
    _print_records([record])


def cmd_verify(args: argparse.Namespace) -> None:
    engine = _engine(args.storage)
    status = engine.integrity_status()
    print(f"Integrity ok: {status['ok']}")
    if status["issues"]:
        print("Issues:")
        for issue in status["issues"]:
            print(f"- {issue}")
    else:
        print(f"Chain length: {status['count']}")


def cmd_summary(args: argparse.Namespace) -> None:
    engine = _engine(args.storage)
    reconstruction = Reconstruction()
    records = engine.list_records()
    policy_view = policy_counts(records)
    latest = reconstruction.latest(records)

    print("Policy distribution:")
    print(ascii_bar(policy_view))
    if latest:
        print("\nLatest record:")
        _print_records([latest])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Glass Substrate demo terminal app")
    parser.add_argument("--storage", help="Optional path to storage.json", default=None)

    sub = parser.add_subparsers(dest="command", required=True)

    list_cmd = sub.add_parser("list", help="List stored records")
    list_cmd.set_defaults(func=cmd_list)

    add_cmd = sub.add_parser("add", help="Add a new record")
    add_cmd.add_argument("--model", required=True, help="Model identifier")
    add_cmd.add_argument("--input-hash", required=True, help="Input hash")
    add_cmd.add_argument("--output-hash", required=True, help="Output hash")
    add_cmd.add_argument("--policy", required=True, help="Policy identifier")
    add_cmd.add_argument("--actor", default="operator", help="Actor submitting the record")
    add_cmd.add_argument("--notes", default="", help="Optional notes")
    add_cmd.set_defaults(func=cmd_add)

    verify_cmd = sub.add_parser("verify", help="Verify the chain integrity")
    verify_cmd.set_defaults(func=cmd_verify)

    summary_cmd = sub.add_parser("summary", help="Show a compact ledger summary")
    summary_cmd.set_defaults(func=cmd_summary)

    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
