"""Non-destructive GSP integrity and control smoke tests (Python 3.10+)."""
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "glass_substrate_demo"))

class GSPSmokeTests(unittest.TestCase):
    def test_original_python_runtime_imports(self):
        import himmu_backup
        self.assertTrue(hasattr(himmu_backup, "GSPGovernanceLogger"))

    def test_seeded_legacy_chain_and_append(self):
        from gsp_core import verify_file, record_event
        sample_path = ROOT / "glass_substrate_demo" / "data" / "sample_events.json"
        data = json.loads(sample_path.read_text(encoding="utf8"))
        with tempfile.TemporaryDirectory() as tmp:
            test_path = pathlib.Path(tmp) / "copy.json"
            test_path.write_text(json.dumps(data), encoding="utf8")
            self.assertTrue(verify_file(str(test_path))["ok"])
            record_event("test", "audit", {"id": "smoke"}, str(test_path))
            self.assertEqual(4, verify_file(str(test_path))["count"])
            changed = json.loads(test_path.read_text(encoding="utf8"))
            changed[0]["action"] = "modified"
            test_path.write_text(json.dumps(changed), encoding="utf8")
            self.assertFalse(verify_file(str(test_path))["ok"])
            with self.assertRaises(ValueError):
                record_event("test", "must-not-append", path=str(test_path))

    def test_engine_chain_and_tamper_detection(self):
        from gsp_core import Engine, Storage, Verification
        with tempfile.TemporaryDirectory() as tmp:
            storage = Storage(pathlib.Path(tmp) / "records.json")
            engine = Engine(storage=storage, verifier=Verification())
            engine.submit(model_id="M", input_hash="a", output_hash="b", policy_id="P")
            self.assertTrue(engine.integrity_status()["ok"])
            state = storage.load()
            state["records"][0]["model_id"] = "altered"
            storage.save_records(state["records"])
            self.assertFalse(engine.integrity_status()["ok"])

    def test_replay_rejects_unknown_step(self):
        from pipeline_replay import ReplayEngine
        from pipeline_serialization import ExecutionTrace, PipelineSerializer, build_execution_trace
        trace = ExecutionTrace(initial_state=[], steps_applied=["unknown"], final_state=[])
        self.assertFalse(ReplayEngine({}).replay(trace).success)
        with self.assertRaises(ValueError):
            PipelineSerializer().load('{"steps":["unknown"]}')
        with self.assertRaises(ValueError):
            build_execution_trace([], ["unknown"])

    def test_web_demo_defaults_local_only(self):
        for name in ("glass_substrate_demo/main.py", "glass_substrate_demo/interfaces/web_dashboard.py"):
            code = (ROOT / name).read_text(encoding="utf8")
            self.assertIn('host="127.0.0.1"', code)
            self.assertIn("debug=False", code)

if __name__ == "__main__":
    unittest.main()
