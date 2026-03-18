
import { useState } from "react";
import Header from "../components/Header";
import { apiRequest } from "../lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [mode, setMode] = useState("login");
  const [message, setMessage] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setMessage("");
    try {
      const path = mode === "login" ? "/auth/login" : "/auth/register";
      const body =
        mode === "login"
          ? { email, password }
          : { email, password, displayName: displayName || email };
      const data = await apiRequest(path, {
        method: "POST",
        body: JSON.stringify(body)
      });
      if (typeof window !== "undefined") {
        localStorage.setItem("gsp_token", data.token);
      }
      setMessage(`Success: ${mode === "login" ? "Logged in" : "Registered"}`);
    } catch (err) {
      setMessage(err.message);
    }
  }

  return (
    <div className="page-shell">
      <Header />
      <main className="page-main">
        <form
          onSubmit={handleSubmit}
          className="glass-card"
          style={{ maxWidth: 420, width: "100%" }}
        >
          <h2 style={{ marginTop: 0 }}>
            {mode === "login" ? "Operator Login" : "Create Operator Account"}
          </h2>

          <label style={{ fontSize: 13 }}>
            Email
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{
                width: "100%",
                marginTop: 4,
                marginBottom: 12,
                padding: 8,
                borderRadius: 8,
                border: "1px solid rgba(255,255,255,0.25)",
                background: "rgba(0,0,0,0.2)",
                color: "#f5f7ff"
              }}
            />
          </label>

          {mode === "register" && (
            <label style={{ fontSize: 13 }}>
              Display name
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                style={{
                  width: "100%",
                  marginTop: 4,
                  marginBottom: 12,
                  padding: 8,
                  borderRadius: 8,
                  border: "1px solid rgba(255,255,255,0.25)",
                  background: "rgba(0,0,0,0.2)",
                  color: "#f5f7ff"
                }}
              />
            </label>
          )}

          <label style={{ fontSize: 13 }}>
            Password
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{
                width: "100%",
                marginTop: 4,
                marginBottom: 16,
                padding: 8,
                borderRadius: 8,
                border: "1px solid rgba(255,255,255,0.25)",
                background: "rgba(0,0,0,0.2)",
                color: "#f5f7ff"
              }}
            />
          </label>

          <button
            type="submit"
            style={{
              width: "100%",
              padding: 10,
              borderRadius: 999,
              border: "none",
              fontWeight: 600,
              cursor: "pointer",
              background:
                "linear-gradient(135deg, #15e6ff, #4f46e5, #9333ea)",
              color: "#fff"
            }}
          >
            {mode === "login" ? "Login" : "Register"}
          </button>

          <div
            style={{
              marginTop: 12,
              fontSize: 12,
              display: "flex",
              justifyContent: "space-between"
            }}
          >
            <span>Mode: {mode}</span>
            <button
              type="button"
              onClick={() =>
                setMode(mode === "login" ? "register" : "login")
              }
              style={{
                background: "none",
                border: "none",
                color: "#15e6ff",
                cursor: "pointer",
                padding: 0,
                fontSize: 12
              }}
            >
              Switch to {mode === "login" ? "register" : "login"}
            </button>
          </div>

          {message && (
            <p style={{ marginTop: 12, fontSize: 12, opacity: 0.9 }}>
              {message}
            </p>
          )}
        </form>
      </main>
      <footer className="page-footer">
        Sierra Warren Developments · Operator Console
      </footer>
    </div>
  );
}
