import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import sqlite3 from "sqlite3";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";

dotenv.config();

const PORT = Number(process.env.PORT || 4000);
const DB_PATH = process.env.DB_PATH || "./gsp.sqlite";
const JWT_SECRET = process.env.JWT_SECRET || "change-me";
const APP_NAME = process.env.APP_NAME || "GSP Reference App";
const ATTESTATION_MODE = process.env.ATTESTATION_MODE || "simulated";

const app = express();
app.use(cors());
app.use(express.json({ limit: "1mb" }));

/* SQLite init */
sqlite3.verbose();
const db = new sqlite3.Database(DB_PATH);

function nowISO() {
  return new Date().toISOString();
}

db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      created_at TEXT NOT NULL
    )
  `);

  db.run(`
    CREATE TABLE IF NOT EXISTS receipts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      model_id TEXT NOT NULL,
      input_hash TEXT NOT NULL,
      output_hash TEXT NOT NULL,
      policy_id TEXT NOT NULL,
      attestation TEXT NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    )
  `);
});

/* Auth middleware */
function requireAuth(req, res, next) {
  const header = req.headers.authorization || "";
  const token = header.startsWith("Bearer ") ? header.slice(7) : null;

  if (!token) return res.status(401).json({ error: "Missing Bearer token" });

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = { id: decoded.sub, email: decoded.email };
    return next();
  } catch {
    return res.status(401).json({ error: "Invalid token" });
  }
}

/* Attestation stub */
function buildAttestation({ userId, modelId, inputHash, outputHash, policyId }) {
  return {
    mode: ATTESTATION_MODE,
    issued_at: nowISO(),
    subject: {
      user_id: String(userId),
      model_id: String(modelId),
      policy_id: String(policyId),
    },
    hashes: { input: String(inputHash), output: String(outputHash) },
    statement:
      "Simulated attestation. Replace with real signing/TEE measurement + audit log anchoring.",
  };
}

/* Routes */
app.get("/health", (_req, res) => {
  res.json({ ok: true, app: APP_NAME, time: nowISO() });
});

app.post("/api/auth/register", (req, res) => {
  const { email, password } = req.body || {};
  if (!email || !password) {
    return res.status(400).json({ error: "email and password required" });
  }

  const createdAt = nowISO();
  const passwordHash = bcrypt.hashSync(password, 10);

  const stmt = db.prepare(
    "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)"
  );

  stmt.run([String(email).toLowerCase(), passwordHash, createdAt], function (err) {
    if (err) {
      if (String(err.message || "").includes("UNIQUE")) {
        return res.status(409).json({ error: "User already exists" });
      }
      return res.status(500).json({ error: "DB error", details: err.message });
    }

    return res.json({
      ok: true,
      user: { id: this.lastID, email: String(email).toLowerCase(), created_at: createdAt },
    });
  });
});

app.post("/api/auth/login", (req, res) => {
  const { email, password } = req.body || {};
  if (!email || !password) {
    return res.status(400).json({ error: "email and password required" });
  }

  db.get(
    "SELECT id, email, password_hash FROM users WHERE email = ?",
    [String(email).toLowerCase()],
    (err, row) => {
      if (err) return res.status(500).json({ error: "DB error", details: err.message });
      if (!row) return res.status(401).json({ error: "Invalid credentials" });

      const ok = bcrypt.compareSync(password, row.password_hash);
      if (!ok) return res.status(401).json({ error: "Invalid credentials" });

      const token = jwt.sign({ email: row.email }, JWT_SECRET, {
        subject: String(row.id),
        expiresIn: "7d",
      });

      return res.json({ ok: true, token });
    }
  );
});

app.post("/api/gsp/submit", requireAuth, (req, res) => {
  const { modelId, inputHash, outputHash, policyId } = req.body || {};
  if (!modelId || !inputHash || !outputHash || !policyId) {
    return res.status(400).json({
      error: "modelId, inputHash, outputHash, policyId are required",
    });
  }

  const createdAt = nowISO();
  const attestation = buildAttestation({
    userId: req.user.id,
    modelId,
    inputHash,
    outputHash,
    policyId,
  });

  const stmt = db.prepare(`
    INSERT INTO receipts
      (user_id, model_id, input_hash, output_hash, policy_id, attestation, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `);

  stmt.run(
    [
      req.user.id,
      String(modelId),
      String(inputHash),
      String(outputHash),
      String(policyId),
      JSON.stringify(attestation),
      createdAt,
    ],
    function (err) {
      if (err) return res.status(500).json({ error: "DB error", details: err.message });
      return res.json({ ok: true, receiptId: this.lastID, createdAt });
    }
  );
});

app.get("/api/gsp/receipt/:id", requireAuth, (req, res) => {
  const id = Number(req.params.id);

  db.get(
    "SELECT * FROM receipts WHERE id = ? AND user_id = ?",
    [id, req.user.id],
    (err, row) => {
      if (err) return res.status(500).json({ error: "DB error", details: err.message });
      if (!row) return res.status(404).json({ error: "Receipt not found" });

      let attestation = null;
      try {
        attestation = JSON.parse(row.attestation);
      } catch {
        attestation = row.attestation;
      }

      return res.json({
        ok: true,
        receipt: {
          id: row.id,
          user_id: row.user_id,
          model_id: row.model_id,
          input_hash: row.input_hash,
          output_hash: row.output_hash,
          policy_id: row.policy_id,
          attestation,
          created_at: row.created_at,
        },
      });
    }
  );
});

app.get("/api/gsp/receipts", requireAuth, (req, res) => {
  db.all(
    "SELECT * FROM receipts WHERE user_id = ? ORDER BY created_at DESC",
    [req.user.id],
    (err, rows) => {
      if (err) return res.status(500).json({ error: "DB error", details: err.message });

      const receipts = (rows || []).map(row => ({
        ...row,
        attestation: JSON.parse(row.attestation || "{}")
      }));

      return res.json({
        ok: true,
        user: { email: req.user.email },
        receipts,
      });
    }
  );
});

app.listen(PORT, () => {
  console.log(`${APP_NAME} backend running on http://0.0.0.0:${PORT}`);
});
