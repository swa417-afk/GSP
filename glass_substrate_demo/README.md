# Glass Substrate Demo

Lightweight Python demo that simulates a glass-substrate style ledger with simple integrity verification, a terminal interface, and a minimal web dashboard.

## Layout
```
glass_substrate_demo/
├── gsp_core/           # Engine, storage, verification, reconstruction helpers
├── interfaces/         # Terminal CLI, notebook starter, web dashboard
├── visualizations/     # Small ASCII chart utilities
├── data/storage.json   # JSON-backed ledger state
├── main.py             # Entrypoint for CLI or web dashboard
└── requirements.txt    # Demo dependencies
```

## Quick start
```bash
cd glass_substrate_demo
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Terminal app
python main.py list
python main.py add --model demo --input-hash in123 --output-hash out456 --policy policy-001
python main.py verify

# Web dashboard
python main.py --web
# visit http://localhost:5055
```

## Notebook
Open `interfaces/notebook_demo.ipynb` to run the same flow interactively. The notebook clears the demo storage and writes two sample records before printing the status.

## Notes
- Records are stored in `data/storage.json` and chained with a simple hash of their contents.
- The terminal `summary` command prints an ASCII bar chart of records per policy.
- The web dashboard offers a compact HTML view and API endpoints for listing and adding records.
