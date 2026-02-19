from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, request

from gsp_core import Engine, Storage, Verification
from visualizations.charts import ascii_bar, policy_counts


def create_app(storage_path: str | None = None) -> Flask:
    storage = Storage(Path(storage_path) if storage_path else None)
    verifier = Verification()
    engine = Engine(storage=storage, verifier=verifier)
    app = Flask(__name__)

    @app.get("/api/records")
    def records() -> Any:
        return jsonify({"records": engine.list_records(), "status": engine.integrity_status()})

    @app.post("/api/records")
    def add_record() -> Any:
        payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
        required = ["model_id", "input_hash", "output_hash", "policy_id"]
        missing = [field for field in required if not payload.get(field)]
        if missing:
            return jsonify({"ok": False, "error": f"Missing fields: {', '.join(missing)}"}), 400

        record = engine.submit(
            model_id=payload["model_id"],
            input_hash=payload["input_hash"],
            output_hash=payload["output_hash"],
            policy_id=payload["policy_id"],
            actor=payload.get("actor", "web"),
            notes=payload.get("notes", ""),
            metadata=payload.get("metadata", {}),
        )
        return jsonify({"ok": True, "record": record}), 201

    @app.get("/")
    def home() -> Any:
        records = engine.list_records()
        status = engine.integrity_status()
        chart = ascii_bar(policy_counts(records))
        template = """
        <html>
        <head>
          <title>Glass Substrate Demo</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 2rem; }
            pre { background: #f5f5f5; padding: 1rem; border-radius: 6px; }
            table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
            th, td { padding: 8px 12px; border: 1px solid #ccc; font-size: 14px; }
            .ok { color: green; }
            .fail { color: red; }
          </style>
        </head>
        <body>
          <h1>Glass Substrate Demo Dashboard</h1>
          <p>Status: <strong class="{{ 'ok' if status['ok'] else 'fail' }}">{{ 'OK' if status['ok'] else 'Attention needed' }}</strong></p>
          <p>Total records: {{ status['count'] }}</p>
          {% if status['issues'] %}
            <h3>Issues</h3>
            <ul>
            {% for issue in status['issues'] %}
              <li>{{ issue }}</li>
            {% endfor %}
            </ul>
          {% endif %}
          <h3>Policy Distribution</h3>
          <pre>{{ chart }}</pre>
          <h3>Records</h3>
          <table>
            <tr>
              <th>ID</th><th>Model</th><th>Policy</th><th>Actor</th><th>Timestamp</th><th>Hash</th>
            </tr>
            {% for record in records %}
            <tr>
              <td>{{ record.record_id[:8] }}</td>
              <td>{{ record.model_id }}</td>
              <td>{{ record.policy_id }}</td>
              <td>{{ record.actor }}</td>
              <td>{{ record.timestamp }}</td>
              <td>{{ record.record_hash[:12] }}</td>
            </tr>
            {% endfor %}
          </table>
        </body>
        </html>
        """
        # Flask can render dicts with dot access; convert to SimpleNamespace-like objects
        class AttrDict(dict):
            __getattr__ = dict.__getitem__

        view_records = [AttrDict(r) for r in records]
        return app.jinja_env.from_string(template).render(
            records=view_records,
            status=status,
            chart=chart,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5055, debug=True)
