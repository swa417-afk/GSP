# Glass Substrate Demo Package

Reference demo showing how to capture, verify, and present Glass Substrate Protocol events using simple JSON artifacts.

## Layout
- `gsp_core/` — core modules for storage, event engine, verification, and timeline reconstruction
- `interfaces/` — terminal CLI, web dashboard, and a notebook stub
- `data/sample_events.json` — seeded event log (append-only hash chain)
- `main.py` — quick entry point to append a sample record and print a summary
- `requirements.txt` — standard-library only demo dependencies

## Quick Start
```bash
# From repo root
PYTHONPATH=. python glass_substrate_demo/main.py
```

### Terminal App
```bash
PYTHONPATH=. python glass_substrate_demo/interfaces/cli.py show
PYTHONPATH=. python glass_substrate_demo/interfaces/cli.py append --actor pilot --action "ingest-policy" --payload '{"policy_id":"pilot-1"}'
PYTHONPATH=. python glass_substrate_demo/interfaces/cli.py verify
```

### Web Dashboard
```bash
cd glass_substrate_demo
python -m http.server 8000
# Open http://localhost:8000/interfaces/dashboard/index.html
```

### Notebook Stub
Open `interfaces/notebook_stub.ipynb` in Jupyter (with `PYTHONPATH` including repo root) to experiment with the core helpers.

## Notes
- Event data is stored as newline-free JSON for easy diffing.
- Hashes are recomputed deterministically from each record body; verification fails fast if anything is edited.
- The demo avoids external dependencies to stay lightweight for pilots and workshops.
