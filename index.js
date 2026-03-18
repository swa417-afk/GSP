
import Header from "../components/Header";

export default function Home() {
  return (
    <div className="page-shell">
      <Header />
      <main className="page-main">
        <div
          className="glass-card"
          style={{
            maxWidth: 720,
            width: "100%",
          }}
        >
          <h1 style={{ marginTop: 0, fontSize: 32 }}>
            Glass Substrate Protocol Control Surface
          </h1>
          <p style={{ fontSize: 15, lineHeight: 1.6 }}>
            This reference console demonstrates how an application can plug
            into the <strong>Glass Substrate Protocol (GSP)</strong>:
            hardware-enforced AI governance, cryptographic attestations, and
            human-centered liability oversight.
          </p>
          <ul style={{ fontSize: 14, lineHeight: 1.7 }}>
            <li>Sign in as an operator using email + password</li>
            <li>Issue GSP-style attestations for key actions</li>
            <li>Query live protocol status from the backend API</li>
          </ul>
          <p style={{ fontSize: 14, opacity: 0.85 }}>
            Branding:{' '}
            <strong>Sierra Warren Developments · Glass Substrate Protocol</strong>
          </p>
        </div>
      </main>
      <footer className="page-footer">
        © {new Date().getFullYear()} Sierra Warren Developments · Glass
        Substrate Protocol v5.0 (reference app)
      </footer>
    </div>
  );
}
