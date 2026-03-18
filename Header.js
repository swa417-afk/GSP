
export default function Header() {
  return (
    <header
      style={{
        padding: "16px 32px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        borderBottom: "1px solid rgba(255,255,255,0.12)",
        backdropFilter: "blur(10px)",
        position: "sticky",
        top: 0,
        zIndex: 10
      }}
    >
      <div>
        <div style={{ fontWeight: 700, letterSpacing: "0.08em" }}>
          SIERRA WARREN DEVELOPMENTS
        </div>
        <div style={{ fontSize: 12, opacity: 0.8 }}>
          Glass Substrate Protocol • Reference Console
        </div>
      </div>
      <nav style={{ display: "flex", gap: 16, fontSize: 14 }}>
        <a href="/">Home</a>
        <a href="/login">Login</a>
        <a href="/dashboard">Dashboard</a>
      </nav>
    </header>
  );
}
