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
