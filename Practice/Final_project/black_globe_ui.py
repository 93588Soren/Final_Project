#!/usr/bin/env python3 #fully ai generate becuase ui is not cool
"""A minimal Python-hosted landing page with an animated wireframe globe.

Run: python black_globe_ui.py
Then open: http://127.0.0.1:8000
No third-party Python packages are required.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import webbrowser

HTML = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#070809" />
  <title>ORBIT — A clearer perspective</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #070809;
      --panel: rgba(15, 17, 19, .72);
      --line: rgba(255, 255, 255, .13);
      --line-bright: rgba(255, 255, 255, .25);
      --text: #f4f5f6;
      --muted: #8d9299;
      --faint: #5b6067;
      --font: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      min-width: 320px;
      background:
        radial-gradient(ellipse at 76% 31%, rgba(110, 121, 136, .10), transparent 31rem),
        radial-gradient(ellipse at 12% 90%, rgba(255, 255, 255, .025), transparent 25rem),
        var(--bg);
      color: var(--text);
      font-family: var(--font);
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 0;
      background-image: linear-gradient(rgba(255,255,255,.022) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255,255,255,.022) 1px, transparent 1px);
      background-size: 58px 58px;
      mask-image: linear-gradient(to bottom, black 0%, transparent 88%);
    }

    a { color: inherit; text-decoration: none; }
    button, input { font: inherit; }
    button, a { -webkit-tap-highlight-color: transparent; }
    .page-shell { position: relative; z-index: 1; width: min(1240px, calc(100% - 64px)); margin: 0 auto; }

    .topbar {
      height: 88px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid rgba(255,255,255,.075);
    }
    .brand { display: inline-flex; align-items: center; gap: 11px; letter-spacing: .22em; font-size: 12px; font-weight: 650; }
    .brand-mark { width: 25px; height: 25px; border: 1px solid rgba(255,255,255,.72); border-radius: 50%; position: relative; display: inline-grid; place-items: center; }
    .brand-mark::before { content: ""; width: 8px; height: 8px; border: 1px solid rgba(255,255,255,.76); border-radius: 50%; }
    .brand-mark::after { content: ""; width: 31px; height: 1px; position: absolute; background: rgba(255,255,255,.38); transform: rotate(-43deg); }
    .nav { display: flex; align-items: center; gap: 35px; color: #9b9fa5; font-size: 12px; }
    .nav a { transition: color .2s ease; }
    .nav a:hover { color: #fff; }
    .nav-cta { border: 1px solid rgba(255,255,255,.24); border-radius: 4px; padding: 11px 15px; color: #f1f2f3 !important; }
    .nav-cta:hover { background: rgba(255,255,255,.07); }

    .hero {
      min-height: 630px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(390px, .93fr);
      align-items: center;
      gap: clamp(44px, 7vw, 100px);
      padding: 66px 0 72px;
    }
    .eyebrow { display: flex; align-items: center; gap: 10px; color: #b4b8bd; font-size: 10px; font-weight: 650; letter-spacing: .19em; text-transform: uppercase; }
    .eyebrow-dot { width: 6px; height: 6px; border-radius: 50%; background: #e9edf0; box-shadow: 0 0 11px rgba(255,255,255,.48); }
    h1 { margin: 25px 0 21px; max-width: 620px; font-size: clamp(56px, 6.2vw, 88px); line-height: .99; letter-spacing: -.075em; font-weight: 510; }
    h1 span { color: #858a91; font-weight: 440; }
    .hero-copy { max-width: 450px; color: var(--muted); font-size: 14px; line-height: 1.9; }
    .actions { display: flex; align-items: center; flex-wrap: wrap; gap: 12px; margin-top: 31px; }
    .button { cursor: pointer; border-radius: 4px; min-height: 46px; padding: 0 17px; display: inline-flex; align-items: center; justify-content: center; gap: 14px; font-size: 12px; font-weight: 600; transition: transform .2s ease, background .2s ease, border-color .2s ease; }
    .button:hover { transform: translateY(-1px); }
    .button-primary { background: #f2f3f4; color: #0a0b0c; border: 1px solid #f2f3f4; }
    .button-primary:hover { background: white; }
    .button-secondary { color: #e4e6e8; border: 1px solid rgba(255,255,255,.18); background: rgba(255,255,255,.018); }
    .button-secondary:hover { border-color: rgba(255,255,255,.35); background: rgba(255,255,255,.045); }
    .arrow { font-size: 16px; line-height: 1; }
    .microcopy { margin-top: 33px; display: flex; align-items: center; gap: 10px; color: #696e75; font-size: 10px; letter-spacing: .045em; }
    .microcopy-line { width: 27px; height: 1px; background: #44494f; }

    .globe-card {
      position: relative;
      isolation: isolate;
      height: min(495px, 39vw);
      min-height: 410px;
      border: 1px solid var(--line);
      border-radius: 7px;
      overflow: hidden;
      background: radial-gradient(ellipse at 50% 45%, rgba(255,255,255,.045), transparent 48%), rgba(10,12,14,.55);
      box-shadow: 0 30px 100px rgba(0,0,0,.24), inset 0 1px rgba(255,255,255,.025);
    }
    .globe-card::before {
      content: ""; position: absolute; inset: 0; pointer-events: none; z-index: -1;
      background: linear-gradient(rgba(255,255,255,.023) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.023) 1px, transparent 1px);
      background-size: 34px 34px;
      mask-image: radial-gradient(ellipse at center, black, transparent 78%);
    }
    .card-top, .card-bottom { position: absolute; left: 22px; right: 22px; display: flex; align-items: center; justify-content: space-between; z-index: 2; }
    .card-top { top: 20px; }
    .card-bottom { bottom: 19px; }
    .card-label { display: flex; flex-direction: column; gap: 5px; }
    .label-kicker { color: #6f757d; font-size: 9px; text-transform: uppercase; letter-spacing: .16em; }
    .label-value { color: #d9dce0; font-size: 10px; letter-spacing: .08em; }
    .coordinate { color: #686e76; font: 10px/1.6 ui-monospace, SFMono-Regular, Menlo, monospace; text-align: right; }
    .live-state { display: inline-flex; align-items: center; gap: 7px; color: #c3c7cc; font-size: 9px; text-transform: uppercase; letter-spacing: .14em; }
    .live-state::before { content: ""; width: 5px; height: 5px; border-radius: 100%; background: #e8edf0; box-shadow: 0 0 8px rgba(255,255,255,.5); }
    .globe-stage { position: absolute; inset: 49px 0 51px; display: grid; place-items: center; }
    #globe { width: min(82%, 340px); height: auto; max-height: 100%; aspect-ratio: 1; overflow: visible; }
    .crosshair { position: absolute; width: 14px; height: 14px; opacity: .45; }
    .crosshair::before, .crosshair::after { content: ""; position: absolute; background: #8b9299; }
    .crosshair::before { left: 6px; width: 1px; height: 14px; }
    .crosshair::after { top: 6px; height: 1px; width: 14px; }
    .crosshair-tl { top: 72px; left: 18px; }
    .crosshair-br { right: 18px; bottom: 72px; }
    .divider { height: 1px; background: var(--line); }
    .stats { display: grid; grid-template-columns: repeat(3, 1fr); padding: 27px 0 34px; }
    .stat { padding: 0 29px; border-left: 1px solid var(--line); }
    .stat:first-child { border-left: 0; padding-left: 0; }
    .stat-value { font-size: 20px; font-weight: 450; letter-spacing: -.04em; }
    .stat-title { margin-top: 7px; color: #777d84; text-transform: uppercase; letter-spacing: .12em; font-size: 9px; }
    .footer { display: flex; justify-content: space-between; padding: 20px 0 29px; color: #5f646b; font-size: 10px; }
    .footer-links { display: flex; gap: 22px; }
    .footer a:hover { color: #d5d8dc; }

    .toast { position: fixed; left: 50%; bottom: 26px; transform: translate(-50%, 16px); opacity: 0; pointer-events: none; border: 1px solid rgba(255,255,255,.18); border-radius: 5px; background: #111315; color: #e5e8eb; padding: 12px 16px; font-size: 12px; box-shadow: 0 12px 45px rgba(0,0,0,.4); transition: opacity .22s ease, transform .22s ease; z-index: 10; }
    .toast.visible { opacity: 1; transform: translate(-50%, 0); }

    @media (max-width: 900px) {
      .page-shell { width: min(100% - 40px, 680px); }
      .hero { grid-template-columns: 1fr; gap: 44px; padding: 75px 0 48px; }
      h1 { font-size: clamp(58px, 11vw, 82px); }
      .globe-card { height: 470px; min-height: 410px; }
      .nav { gap: 18px; }
      .hero-copy { max-width: 520px; }
    }
    @media (max-width: 560px) {
      .page-shell { width: calc(100% - 36px); }
      .topbar { height: 72px; }
      .nav a:not(.nav-cta) { display: none; }
      .nav { gap: 0; }
      .nav-cta { padding: 10px 12px; }
      .hero { padding-top: 63px; gap: 38px; }
      h1 { font-size: clamp(51px, 13.1vw, 70px); }
      .hero-copy { font-size: 13px; }
      .globe-card { height: 390px; min-height: 360px; }
      .card-top, .card-bottom { left: 15px; right: 15px; }
      .crosshair-tl { left: 12px; }
      .crosshair-br { right: 12px; }
      .stats { gap: 0; padding-top: 22px; }
      .stat { padding: 0 12px; }
      .stat-value { font-size: 17px; }
      .stat-title { font-size: 8px; line-height: 1.5; }
      .footer { gap: 18px; flex-wrap: wrap; }
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; }
    }
  </style>
</head>
<body>
  <div class="page-shell">
    <header class="topbar">
      <a class="brand" href="#top" aria-label="Orbit home"><span class="brand-mark" aria-hidden="true"></span><span>SOREN WISMAR'S PROGRAM</span></a>
      <nav class="nav" aria-label="Main navigation">
        <a href="#overview">Overview</a>
        <a href="#signal">Signal</a>
        <a class="nav-cta" href="#connect">Get in touch <span aria-hidden="true">↗</span></a>
      </nav>
    </header>

    <main id="top">
      <section class="hero" id="overview">
        <div class="hero-content">
          <div class="eyebrow"><span class="eyebrow-dot"></span> A NEW PERSPECTIVE</div>
          <h1>Look beyond<br />the <span>ordinary.</span></h1>
          <p class="hero-copy">A short introduction to your product or idea goes here. Use this space to explain what you do, who it helps, and why it matters.</p>
          <div class="actions">
            <a class="button button-primary" href="#connect">Explore the platform <span class="arrow" aria-hidden="true">↗</span></a>
            <button class="button button-secondary" id="scan-button" type="button">Run a scan <span class="arrow" aria-hidden="true">↗</span></button>
          </div>
          <div class="microcopy"><span class="microcopy-line"></span> BUILT FOR A WIDER VIEW</div>
        </div>

        <div class="globe-card" id="signal" aria-label="Animated wireframe globe visualization">
          <div class="card-top">
            <div class="card-label"><span class="label-kicker">Live visualization</span><span class="label-value">GLOBAL MESH / 001</span></div>
            
          </div>
          <span class="crosshair crosshair-tl" aria-hidden="true"></span>
          <span class="crosshair crosshair-br" aria-hidden="true"></span>
          <div class="globe-stage">
            <canvas id="globe" role="img" aria-label="A globe of fine white lines slowly rotating in space"></canvas>
          </div>
          <div class="card-bottom">
            <div class="card-label"><span class="label-kicker">Network status</span><span class="label-value">ALL SYSTEMS NOMINAL</span></div>
            <span class="live-state">ONLINE</span>
          </div>
        </div>
      </section>

      <div class="divider"></div>
      <section class="stats" aria-label="Platform highlights">
        <div class="stat"><div class="stat-value">01 — 24</div><div class="stat-title">A simple metric goes here</div></div>
        <div class="stat"><div class="stat-value">Global</div><div class="stat-title">Made for the bigger picture</div></div>
        <div class="stat"><div class="stat-value">Always on</div><div class="stat-title">Connected by design</div></div>
      </section>
      <div class="divider"></div>

      <footer class="footer" id="connect">
        <span>© 2026 ORBIT STUDIO. YOUR STORY STARTS HERE.</span>
        <div class="footer-links"><a href="#overview">Overview</a><a href="mailto:hello@example.com">Contact</a></div>
      </footer>
    </main>
  </div>
  <div class="toast" id="toast" role="status" aria-live="polite">Preview action triggered — connect your scan workflow here.</div>

  <script>
    (() => {
      const canvas = document.getElementById('globe');
      const ctx = canvas.getContext('2d');
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      let width = 0, height = 0, dpr = 1, frame = 0;
      const TAU = Math.PI * 2;

      function resize() {
        const rect = canvas.getBoundingClientRect();
        if (!rect.width || !rect.height) return;
        width = rect.width;
        height = rect.height;
        dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = Math.round(width * dpr);
        canvas.height = Math.round(height * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      }

      function project(lat, lon, rotation, cx, cy, radius) {
        const angle = lon + rotation;
        const cosLat = Math.cos(lat);
        return {
          x: cx + radius * cosLat * Math.sin(angle),
          y: cy - radius * Math.sin(lat),
          z: cosLat * Math.cos(angle)
        };
      }

      // Render the front hemisphere in crisp white and the far side as a faint trace.
      function strokeWire(points) {
        const front = new Path2D();
        const back = new Path2D();
        for (let i = 0; i < points.length - 1; i++) {
          const a = points[i], b = points[i + 1];
          const path = ((a.z + b.z) * .5 >= 0) ? front : back;
          path.moveTo(a.x, a.y);
          path.lineTo(b.x, b.y);
        }
        ctx.lineWidth = .78;
        ctx.strokeStyle = 'rgba(239, 243, 247, .39)';
        ctx.stroke(front);
        ctx.strokeStyle = 'rgba(197, 205, 214, .105)';
        ctx.stroke(back);
      }

      function draw(timestamp) {
        if (!width || !height) resize();
        ctx.clearRect(0, 0, width, height);
        const cx = width / 2;
        const cy = height / 2;
        const radius = Math.min(width, height) * .385;
        const rotation = (reducedMotion ? 0 : timestamp * .00016) + .35;

        const halo = ctx.createRadialGradient(cx, cy, radius * .12, cx, cy, radius * 1.45);
        halo.addColorStop(0, 'rgba(200, 211, 224, .065)');
        halo.addColorStop(.72, 'rgba(110, 124, 140, .022)');
        halo.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = halo;
        ctx.fillRect(0, 0, width, height);

        // Meridians.
        const meridianCount = 18;
        for (let m = 0; m < meridianCount; m++) {
          const lon = (m / meridianCount) * TAU;
          const points = [];
          for (let s = 0; s <= 100; s++) {
            const lat = -Math.PI / 2 + (s / 100) * Math.PI;
            points.push(project(lat, lon, rotation, cx, cy, radius));
          }
          strokeWire(points);
        }

        // Latitude rings.
        for (let ring = -5; ring <= 5; ring++) {
          const lat = ring * (Math.PI / 13);
          const points = [];
          for (let s = 0; s <= 144; s++) {
            const lon = (s / 144) * TAU;
            points.push(project(lat, lon, rotation, cx, cy, radius));
          }
          strokeWire(points);
        }

        // Outer silhouette and a tiny axis marker keep the globe sharply defined.
        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, TAU);
        ctx.lineWidth = .95;
        ctx.strokeStyle = 'rgba(237, 241, 245, .50)';
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(cx + radius * .48 * Math.sin(rotation * 1.7), cy - radius * .14, 1.8, 0, TAU);
        ctx.fillStyle = 'rgba(255,255,255,.86)';
        ctx.fill();

        if (!reducedMotion) frame = requestAnimationFrame(draw);
      }

      const observer = new ResizeObserver(() => { resize(); });
      observer.observe(canvas);
      resize();
      frame = requestAnimationFrame(draw);
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) cancelAnimationFrame(frame);
        else if (!reducedMotion) frame = requestAnimationFrame(draw);
      });

      const scanButton = document.getElementById('scan-button');
      const toast = document.getElementById('toast');
      scanButton.addEventListener('click', () => {
        toast.classList.add('visible');
        window.clearTimeout(scanButton._toastTimer);
        scanButton._toastTimer = window.setTimeout(() => toast.classList.remove('visible'), 2600);
      });
    })();
  </script>
</body>
</html>'''


class PageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404, "Not found")
            return
        content = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        # Keep the terminal output clean; the server still handles errors normally.
        pass


def main():
    parser = argparse.ArgumentParser(description="Serve the ORBIT black-globe UI locally.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port number (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open a browser")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), PageHandler)
    url = f"http://{args.host}:{args.port}"
    print(f"ORBIT UI is running at {url}")
    print("Press Ctrl+C to stop the server.")
    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping ORBIT UI...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
