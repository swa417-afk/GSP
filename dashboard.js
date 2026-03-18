
import { useState } from "react";
import Header from "../components/Header";
import { apiRequest } from "../lib/api";

export default function Dashboard() {
  const [status, setStatus] = useState(null);
  const [actionName, setActionName] = useState("MODEL_INVOKE");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function fetchStatus() {
    setError("");
    try {
      const data = await apiRequest("/gsp/status");
      setStatus(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function logAction() {
    setError("");
    try {
      const data = await apiRequest("/gsp/actions/log", {
        method: "POST",
        body: JSON.stringify({
          action: actionName,
          metadata: {
            origin: "frontend-dashboard",
            description: "Sample action logged from Sierra's console"
          }
        })
      });
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="page-shell">
      <Header />
      <main className="page-main">
        <div
          className="glass-card"
          style={{
            maxWidth: 900,
            width: "100%",
            display: "grid",
            gridTemplateColumns: "minmax(0, 1.2fr) minmax(0, 1fr)",
            gap: 24
          }}
        >
          <section>
            <h2 style={{ marginTop: 0 }}>Operator Dashboard</h2>
            <p style={{ fontSize: 14, lineHeight: 1.7 }}>
              Use this panel to perform GSP-governed actions, generate
              attestations, and inspect protocol status. In a production
              deployment this surface would sit on top of secure hardware
              and a full liability registry.
            </p>
            <div style={{ marginTop: 16 }}>
              <button
                onClick={fetchStatus}
                style={{
                  padding: "8px 14px",
                  borderRadius: 999,
                  border: "none",
                  background: "#15e6ff",
                  color: "#050816",
                  fontWeight: 600,
                  cursor: "pointer",
                  marginRight: 8
                }}
              >
                Check GSP status
              </button>
              <button
                onClick={logAction}
                style={{
                  padding: "8px 14px",
                  borderRadius: 999,
                  border: "1px solid rgba(255,255,255,0.4)",
                  background: "transparent",
                  color: "#f5f7ff",
                  fontWeight: 500,
                  cursor: "pointer"
                }}
              >
                Log sample action
              </button>
            </div>

            <div style={{ marginTop: 16 }}>
              <label style={{ fontSize: 13 }}>
                Action name
                <input
                  type="text"
                  value={actionName}
                  onChange={(e) => setActionName(e.target.value)}
                  style={{
                    width: "100%",
                    marginTop: 4,
                    padding: 8,
                    borderRadius: 8,
                    border: "1px solid rgba(255,255,255,0.25)",
                    background: "rgba(0,0,0,0.2)",
                    color: "#f5f7ff"
                  }}
                />
              </label>
            </div>

            {error && (
              <p style={{ marginTop: 16, fontSize: 13, color: "#ffb4b4" }}>
                Error: {error}
              </p>
            )}
          </section>

          <section
            style={{
              fontSize: 12,
              background: "rgba(0,0,0,0.28)",
              borderRadius: 12,
              padding: 12,
              border: "1px solid rgba(255,255,255,0.18)",
              overflow: "auto",
              maxHeight: 360
            }}
          >
            <h3 style={{ marginTop: 0, fontSize: 13 }}>Live JSON feed</h3>
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {status
                ? JSON.stringify({ status }, null, 2)
                : "Status not loaded yet."}
            </pre>
            <hr style={{ borderColor: "rgba(255,255,255,0.1)" }} />
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {result
                ? JSON.stringify({ lastAction: result }, null, 2)
                : "No action logged yet."}
            </pre>
          </section>
        </div>
      </main>
      <footer className="page-footer">
        GSP Liability Oversight Console · Reference Only
      </footer>
    </div>
  );
}
