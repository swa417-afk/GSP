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
