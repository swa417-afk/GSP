"""Non-destructive checks for first-stage GSP credential containment."""
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class CredentialContainmentTests(unittest.TestCase):
    def test_env_is_not_git_tracked(self):
        result = subprocess.run(["git", "ls-files", "--", ".env"], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        self.assertFalse(result.stdout.strip(), ".env must not be committed")

    def test_example_has_no_jwt_value(self):
        for line in (ROOT / ".env.example").read_text(encoding="utf8").splitlines():
            if line.startswith("JWT_SECRET="):
                self.assertEqual(line, "JWT_SECRET=")
                return
        self.fail("JWT_SECRET example entry missing")

    def test_backend_fails_closed_and_limits_cors(self):
        server = (ROOT / "server.js").read_text(encoding="utf8")
        self.assertNotIn('JWT_SECRET || "change-me"', server)
        self.assertIn('throw new Error("Set JWT_SECRET', server)
        self.assertIn("GSP_ALLOWED_ORIGINS.includes(origin)", server)
        self.assertIn('GSP_HOST || "127.0.0.1"', server)

    def test_test_runner_redacts_token(self):
        script = (ROOT / "test_api.sh").read_text(encoding="utf8")
        self.assertNotIn('echo "$LOGIN_RESPONSE" | jq .', script)

if __name__ == "__main__":
    unittest.main()
