const http = require('http');
const { URL } = require('url');

const rawPort = process.env.PORT;
const parsedPort = rawPort !== undefined ? Number.parseInt(rawPort, 10) : NaN;
const port =
  Number.isInteger(parsedPort) && parsedPort >= 1 && parsedPort <= 65535
    ? parsedPort
    : 8080;
const host = '0.0.0.0';

const server = http.createServer((req, res) => {
  const { method, url } = req;
  const pathname = new URL(url, 'http://localhost').pathname;
  res.on('finish', () => {
    console.log(`[request] ${method} ${pathname} -> ${res.statusCode}`);
  });

  if (method === 'GET' && pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<!doctype html><html><body><h1>tradingq up ✅</h1></body></html>');
    return;
  }

  if (method === 'GET' && pathname === '/healthz') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ ok: true }));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('Not Found');
});

server
  .listen(port, host, () => {
    console.log(`[startup] server listening on http://${host}:${port}`);
  })
  .on('error', (err) => {
    console.error('[startup] failed to start server:', err);
    process.exit(1);
  });

const shutdownSignals = ['SIGTERM', 'SIGINT'];
const shutdownTimeoutMs = 10000;

shutdownSignals.forEach((signal) => {
  process.on(signal, () => {
    console.log(`[shutdown] received ${signal}, closing server`);

    const forceShutdownTimeout = setTimeout(() => {
      console.error('[shutdown] forcing shutdown after timeout');
      process.exit(1);
    }, shutdownTimeoutMs);

    if (typeof forceShutdownTimeout.unref === 'function') {
      forceShutdownTimeout.unref();
    }

    server.close((err) => {
      if (err) {
        console.error('[shutdown] error while closing server:', err);
        process.exit(1);
      }

      console.log('[shutdown] server closed gracefully');
      process.exit(0);
    });
  });
});

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
