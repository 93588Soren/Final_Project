from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import numpy as np
import KNN
import logistical_reg


HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOREN WISMAR</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            background: #050505;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }

        .page {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 35px 20px;
        }

        h1 {
            margin: 0 0 35px;
            font-size: clamp(25px, 4vw, 42px);
            letter-spacing: 8px;
            font-weight: 400;
            text-align: center;
        }

        .layout {
            width: 100%;
            max-width: 950px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 35px;
            align-items: center;
        }

        .globe-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-width: 0;
        }

        canvas {
            width: 100%;
            max-width: 430px;
            aspect-ratio: 1;
            display: block;
        }

        .form-container {
            width: 100%;
            padding: 25px;
            border: 1px solid #292929;
            border-radius: 12px;
            background: #0a0a0a;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .field {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .field.wide {
            grid-column: 1 / -1;
        }

        label {
            color: #bdbdbd;
            font-size: 12px;
        }

        input {
            width: 100%;
            min-width: 0;
            padding: 12px;
            border: 1px solid #333333;
            border-radius: 6px;
            outline: none;
            background: #111111;
            color: #ffffff;
            font-size: 14px;
        }

        input:focus {
            border-color: #aaaaaa;
        }

        button {
            width: 100%;
            margin-top: 22px;
            padding: 14px;
            border: 1px solid #ffffff;
            border-radius: 6px;
            background: #ffffff;
            color: #050505;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #d8d8d8;
        }

        button:disabled {
            cursor: wait;
            opacity: 0.6;
        }

        #result {
            min-height: 24px;
            margin-top: 18px;
            color: #ffffff;
            font-size: 14px;
            line-height: 1.7;
            overflow-wrap: anywhere;
        }

        .verdict {
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .note {
            margin-top: 4px;
            color: #8a8a8a;
            font-size: 12px;
            line-height: 1.5;
        }

        @media (max-width: 700px) {
            .layout {
                grid-template-columns: 1fr;
                gap: 10px;
                max-width: 450px;
            }

            canvas {
                max-width: 300px;
            }

            h1 {
                margin-bottom: 20px;
            }
        }

        @media (max-width: 380px) {
            .form-grid {
                grid-template-columns: 1fr;
            }

            .form-container {
                padding: 18px;
            }
        }
    </style>
</head>

<body>
    <main class="page">
        <h1>SOREN WISMAR</h1>

        <div class="layout">
            <div class="globe-container">
                <canvas id="globe"></canvas>
            </div>

            <section class="form-container">
                <form id="asteroidForm">
                    <div class="form-grid">
                        <div class="field">
                            <label for="diameter_km">Diameter (km)</label>
                            <input id="diameter_km" name="diameter_km"
                                   type="number" step="any" required>
                        </div>

                        <div class="field">
                            <label for="H">Absolute magnitude (H)</label>
                            <input id="H" name="H"
                                   type="number" step="any" required>
                        </div>

                        <div class="field">
                            <label for="e">Orbital eccentricity</label>
                            <input id="e" name="e"
                                   type="number" step="any" required>
                        </div>

                        <div class="field">
                            <label for="q">Perihelion distance</label>
                            <input id="q" name="q"
                                   type="number" step="any" required>
                        </div>

                        <div class="field wide">
                            <label for="moid_km">
                                Minimum orbit intersection distance
                            </label>
                            <input id="moid_km" name="moid_km"
                                   type="number" step="any" required>
                        </div>
                    </div>

                    <button id="predictButton" type="submit">
                        Predict
                    </button>

                    <div id="result" role="status" aria-live="polite"></div>
                </form>
            </section>
        </div>
    </main>

    <script>
        const canvas = document.getElementById("globe");
        const ctx = canvas.getContext("2d");

        // ---------- Settings ----------
        const TILT = 0.2;              // how far the globe is tipped toward us (radians)
        const SPIN = 0.18;             // globe rotation speed (radians per second)
        const FLIGHT_TIME = 1.6;       // seconds the asteroid takes to arrive
        const AFTERMATH_TIME = 2.7;    // seconds the impact effect lasts
        const ASTEROID_SIZE = 0.2;     // asteroid radius, in globe radii

        const COS_T = Math.cos(TILT);
        const SIN_T = Math.sin(TILT);

        let angle = 0;     // current globe rotation
        let clock = 0;     // seconds since the page started
        let size = 0;      // canvas size in CSS pixels
        let impact = null; // the asteroid animation, or null when idle

        function resizeCanvas() {
            size = canvas.clientWidth;
            const pixelRatio = window.devicePixelRatio || 1;

            canvas.width = size * pixelRatio;
            canvas.height = size * pixelRatio;

            ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
        }

        // ---------- 3D helpers ----------
        // World space: x = right, y = up, z = toward the viewer, globe radius = 1.
        function project(p) {
            const y = p[1] * COS_T - p[2] * SIN_T;
            const z = p[1] * SIN_T + p[2] * COS_T;
            const center = size / 2;
            const radius = size * 0.36;

            return { x: center + p[0] * radius, y: center - y * radius, z: z };
        }

        function cross(a, b) {
            return [
                a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0]
            ];
        }

        function normalize(v) {
            const length = Math.hypot(v[0], v[1], v[2]);
            return [v[0] / length, v[1] / length, v[2] / length];
        }

        // A point on the globe's surface, given its fixed latitude/longitude
        // on the globe and how far the globe has rotated.
        function surfacePoint(lat, localLon, rotation) {
            const lon = localLon + rotation;
            return [
                Math.cos(lat) * Math.sin(lon),
                Math.sin(lat),
                Math.cos(lat) * Math.cos(lon)
            ];
        }

        // Stroke a line through 3D points. With frontOnly, the parts on the
        // far side of the globe are skipped.
        function strokeLine(points, frontOnly) {
            ctx.beginPath();
            let penDown = false;

            for (const point of points) {
                const s = project(point);

                if (frontOnly && s.z < 0) {
                    penDown = false;
                    continue;
                }

                if (penDown) {
                    ctx.lineTo(s.x, s.y);
                } else {
                    ctx.moveTo(s.x, s.y);
                    penDown = true;
                }
            }

            ctx.stroke();
        }

        // ---------- Globe ----------
        function drawGlobe() {
            ctx.strokeStyle = "rgba(210, 210, 210, 0.42)";
            ctx.lineWidth = 0.7;

            // Latitude lines
            for (let lat = -75; lat <= 75; lat += 15) {
                const latitude = lat * Math.PI / 180;
                const points = [];

                for (let step = 0; step <= 72; step++) {
                    const t = step / 72 * Math.PI * 2;
                    points.push([
                        Math.cos(latitude) * Math.cos(t),
                        Math.sin(latitude),
                        Math.cos(latitude) * Math.sin(t)
                    ]);
                }

                strokeLine(points, false);
            }

            // Longitude lines: each one is a half circle from pole to pole,
            // so we need all 24 (every 15 degrees through a full 360) to
            // cover the whole globe.
            for (let lon = 0; lon < 360; lon += 15) {
                const longitude = lon * Math.PI / 180 + angle;
                const points = [];

                for (let step = 0; step <= 60; step++) {
                    const latitude = (step / 60 - 0.5) * Math.PI;
                    points.push([
                        Math.cos(latitude) * Math.sin(longitude),
                        Math.sin(latitude),
                        Math.cos(latitude) * Math.cos(longitude)
                    ]);
                }

                strokeLine(points, false);
            }
        }

        // ---------- Wireframe asteroid ----------
        // A lumpy wireframe rock: an icosahedron split once (42 points),
        // with every point pushed in or out by a random amount.
        function buildAsteroid() {
            const t = (1 + Math.sqrt(5)) / 2;
            const verts = [
                [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
                [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
                [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]
            ];
            const faces = [
                [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
                [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
                [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
                [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
            ];

            const midpoints = {};
            function midpoint(a, b) {
                const key = a < b ? a + "_" + b : b + "_" + a;

                if (!(key in midpoints)) {
                    verts.push([
                        (verts[a][0] + verts[b][0]) / 2,
                        (verts[a][1] + verts[b][1]) / 2,
                        (verts[a][2] + verts[b][2]) / 2
                    ]);
                    midpoints[key] = verts.length - 1;
                }

                return midpoints[key];
            }

            const triangles = [];
            for (const [a, b, c] of faces) {
                const ab = midpoint(a, b);
                const bc = midpoint(b, c);
                const ca = midpoint(c, a);
                triangles.push([a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]);
            }

            const edgeSet = new Set();
            const edges = [];
            for (const [a, b, c] of triangles) {
                for (const [p, q] of [[a, b], [b, c], [c, a]]) {
                    const key = p < q ? p + "_" + q : q + "_" + p;
                    if (!edgeSet.has(key)) {
                        edgeSet.add(key);
                        edges.push([p, q]);
                    }
                }
            }

            const lumpy = verts.map(function(v) {
                const unit = normalize(v);
                const bump = 0.7 + Math.random() * 0.5;
                return [unit[0] * bump, unit[1] * bump * 0.85, unit[2] * bump];
            });

            return { verts: lumpy, edges: edges };
        }

        function drawAsteroid(position, scale, spin, alpha) {
            const mesh = impact.mesh;
            const cy = Math.cos(spin), sy = Math.sin(spin);
            const cx = Math.cos(spin * 0.6), sx = Math.sin(spin * 0.6);

            const projected = mesh.verts.map(function(v) {
                // Tumble: spin around Y, then around X.
                const x = v[0] * cy + v[2] * sy;
                const z = -v[0] * sy + v[2] * cy;
                const y2 = v[1] * cx - z * sx;
                const z2 = v[1] * sx + z * cx;

                return project([
                    position[0] + x * scale,
                    position[1] + y2 * scale,
                    position[2] + z2 * scale
                ]);
            });

            ctx.strokeStyle = "rgba(255, 255, 255, " + alpha + ")";
            ctx.lineWidth = 0.9;
            ctx.beginPath();

            for (const [a, b] of mesh.edges) {
                ctx.moveTo(projected[a].x, projected[a].y);
                ctx.lineTo(projected[b].x, projected[b].y);
            }

            ctx.stroke();
        }

        // Where the asteroid is, from 0 (start) to 1 (impact). It speeds up
        // as it falls, and it homes in on the impact spot as the globe turns.
        function asteroidPosition(progress) {
            const target = surfacePoint(impact.lat, impact.localLon, angle);
            const eased = progress * progress;

            return [0, 1, 2].map(function(k) {
                return impact.start[k] + (target[k] - impact.start[k]) * eased;
            });
        }

        function startImpact() {
            // Pick a spot that will be on the visible side when the asteroid lands.
            const lat = (Math.random() - 0.5) * 50 * Math.PI / 180;
            const viewLon = (Math.random() - 0.5) * 70 * Math.PI / 180;
            const rotationAtImpact = angle + SPIN * FLIGHT_TIME;
            const localLon = viewLon - rotationAtImpact;

            // Start in a top corner of the canvas, outside the globe's outline,
            // and fly across to the impact spot. The start height (z) is chosen
            // so the path stays outside the globe the whole way in.
            const normal = surfacePoint(lat, localLon, rotationAtImpact);
            const farSide = normal[0] > 0 ? -1 : 1;
            let start = null;

            for (const side of [farSide, -farSide]) {
                const z = (1.4 - side * 1.3 * normal[0] - 1.25 * normal[1]) / normal[2];

                if (z <= 3.5 || side !== farSide) {
                    start = [side * 1.3, 1.25, Math.max(1.0, z)];
                    break;
                }
            }

            impact = {
                startTime: clock,
                lat: lat,
                localLon: localLon,
                start: start,
                mesh: buildAsteroid()
            };
        }

        function drawRing(angularRadius, alpha) {
            const normal = surfacePoint(impact.lat, impact.localLon, angle);
            const u = normalize(cross([0, 1, 0], normal));
            const v = cross(normal, u);
            const c = Math.cos(angularRadius);
            const s = Math.sin(angularRadius);
            const points = [];

            for (let step = 0; step <= 72; step++) {
                const a = step / 72 * Math.PI * 2;
                points.push([0, 1, 2].map(function(k) {
                    return normal[k] * c + (u[k] * Math.cos(a) + v[k] * Math.sin(a)) * s;
                }));
            }

            ctx.strokeStyle = "rgba(255, 255, 255, " + alpha + ")";
            ctx.lineWidth = 1.4;
            strokeLine(points, true);
        }

        function drawImpact() {
            const age = clock - impact.startTime;

            // Flight
            if (age < FLIGHT_TIME) {
                const progress = age / FLIGHT_TIME;
                const position = asteroidPosition(progress);
                const here = project(position);
                const before = project(asteroidPosition(Math.max(0, progress - 0.12)));

                // Short fading tail behind the asteroid
                const tail = ctx.createLinearGradient(before.x, before.y, here.x, here.y);
                tail.addColorStop(0, "rgba(255, 255, 255, 0)");
                tail.addColorStop(1, "rgba(255, 255, 255, 0.5)");
                ctx.strokeStyle = tail;
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(before.x, before.y);
                ctx.lineTo(here.x, here.y);
                ctx.stroke();

                // Fade in so it doesn't pop into view at the edge of the canvas
                const alpha = Math.min(1, progress / 0.15) * 0.95;
                const scale = ASTEROID_SIZE * (0.6 + 0.4 * progress);
                drawAsteroid(position, scale, age * 3, alpha);
                return;
            }

            // Aftermath: a flash, then shockwave rings spreading over the surface
            const after = age - FLIGHT_TIME;

            if (after > AFTERMATH_TIME) {
                impact = null;
                return;
            }

            const flashAlpha = Math.max(0, 1 - after / 0.35);

            if (flashAlpha > 0) {
                const spot = project(surfacePoint(impact.lat, impact.localLon, angle));
                const flashRadius = size * 0.09;
                const glow = ctx.createRadialGradient(
                    spot.x, spot.y, 0, spot.x, spot.y, flashRadius
                );
                glow.addColorStop(0, "rgba(255, 255, 255, " + flashAlpha + ")");
                glow.addColorStop(1, "rgba(255, 255, 255, 0)");
                ctx.fillStyle = glow;
                ctx.beginPath();
                ctx.arc(spot.x, spot.y, flashRadius, 0, Math.PI * 2);
                ctx.fill();
            }

            for (let ring = 0; ring < 3; ring++) {
                const ringAge = after - ring * 0.3;
                const life = ringAge / 2.0;

                if (ringAge <= 0 || life >= 1) {
                    continue;
                }

                const spread = 0.6 * (1 - (1 - life) * (1 - life));
                drawRing(spread, (1 - life) * 0.9);
            }
        }

        // ---------- Animation loop ----------
        let lastFrame = performance.now();

        function frame(now) {
            const dt = Math.min((now - lastFrame) / 1000, 0.05);
            lastFrame = now;

            clock += dt;
            angle += SPIN * dt;

            ctx.clearRect(0, 0, size, size);
            drawGlobe();

            if (impact) {
                drawImpact();
            }

            requestAnimationFrame(frame);
        }

        resizeCanvas();
        window.addEventListener("resize", resizeCanvas);
        requestAnimationFrame(frame);

        // ---------- Submit asteroid data to Python ----------
        const form = document.getElementById("asteroidForm");
        const result = document.getElementById("result");
        const predictButton = document.getElementById("predictButton");

        form.addEventListener("submit", async function(event) {
            event.preventDefault();

            const formData = new FormData(form);
            const asteroid = {};

            for (const [key, value] of formData.entries()) {
                asteroid[key] = Number(value);
            }

            result.textContent = "Calculating...";
            predictButton.disabled = true;
            impact = null;

            try {
                const response = await fetch("/predict", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(asteroid)
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || "Prediction failed.");
                }

                result.replaceChildren();

                const verdict = document.createElement("div");
                verdict.className = "verdict";
                verdict.textContent =
                    "Is asteroid harmful: " + (data.harmful ? "YES" : "NO");
                result.appendChild(verdict);

                if (data.note) {
                    const note = document.createElement("div");
                    note.className = "note";
                    note.textContent = data.note;
                    result.appendChild(note);
                }

                if (data.harmful) {
                    startImpact();
                }

            } catch (error) {
                result.textContent = "Error: " + error.message;
            } finally {
                predictButton.disabled = false;
            }
        });
    </script>
</body>
</html>
"""


# Feature order must match the order used to train both models.
FEATURES = [
    "diameter_km",
    "H",
    "e",
    "q",
    "moid_km",
]

# Physically possible range for each input (label, lowest, highest).
# Values outside these, like 0 in every field, can't be a real near-Earth
# asteroid, and the models would only be guessing, so they are rejected.
LIMITS = {
    "diameter_km": ("Diameter (km)", 0.0001, 100),
    "H": ("Absolute magnitude (H)", 5, 40),
    "e": ("Orbital eccentricity", 0, 0.9999),
    "q": ("Perihelion distance", 0.01, 1.3),
    "moid_km": ("Minimum orbit intersection distance", 0, 300000000),
}

# What to do when the two models disagree (a 1-1 tie):
#   "harmful"      -> say YES   (safest: a false alarm is better than a miss)
#   "not_harmful"  -> say NO
#   "knn"          -> go with KNN's answer
TIE_RULE = "harmful"

TIE_NOTES = {
    "harmful": "The two models disagreed, so it was flagged as harmful to be safe.",
    "not_harmful": "The two models disagreed, so it was not flagged as harmful.",
    "knn": "The two models disagreed, so the KNN model's answer was used.",
}


def decide(knn_vote, logistic_vote):
    """Combine the two votes into one yes/no. Returns (harmful, note)."""
    if knn_vote == logistic_vote:
        return bool(knn_vote), None

    # The models disagree: a tie.
    if TIE_RULE == "harmful":
        harmful = True
    elif TIE_RULE == "not_harmful":
        harmful = False
    else:
        harmful = bool(knn_vote)

    return harmful, TIE_NOTES[TIE_RULE]


def run_predictions(new_asteroid):
    new_asteroid = np.asarray(new_asteroid, dtype=float).reshape(-1)

    if len(new_asteroid) != len(FEATURES):
        raise ValueError(f"Exactly {len(FEATURES)} asteroid measurements are required.")

    if not np.all(np.isfinite(new_asteroid)):
        raise ValueError("All measurements must be finite numbers.")

    problems = []
    for name, value in zip(FEATURES, new_asteroid):
        label, low, high = LIMITS[name]
        if not low <= value <= high:
            problems.append(f"{label} must be between {low:,.10g} and {high:,.10g}")

    if problems:
        raise ValueError("; ".join(problems) + ".")

    knn_result = KNN.predict(new_asteroid)
    logistic_result = logistical_reg.predict(new_asteroid)

    # Support either a scalar or a one-element NumPy array.
    knn_result = int(np.asarray(knn_result).item())
    logistic_result = int(np.asarray(logistic_result).item())

    harmful, note = decide(knn_result, logistic_result)

    print(f"[Votes] KNN={knn_result}  Logistic={logistic_result}  -> harmful={harmful}")

    return {
        "harmful": harmful,
        "note": note,
    }


class PageHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Page not found")
            return

        body = HTML.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/predict":
            self.send_json(404, {"error": "Endpoint not found."})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))

            if content_length <= 0 or content_length > 10000:
                self.send_json(400, {"error": "Invalid request size."})
                return

            raw_body = self.rfile.read(content_length)
            data = json.loads(raw_body.decode("utf-8"))

            if not isinstance(data, dict):
                self.send_json(400, {"error": "Expected asteroid measurements."})
                return

            # Require all named inputs.
            if any(name not in data for name in FEATURES):
                self.send_json(
                    400,
                    {"error": f"Please provide all {len(FEATURES)} measurements."}
                )
                return

            new_asteroid = np.array(
                [float(data[name]) for name in FEATURES],
                dtype=float
            )

            if not np.all(np.isfinite(new_asteroid)):
                self.send_json(400, {"error": "Measurements must be finite numbers."})
                return

            predictions = run_predictions(new_asteroid)
            self.send_json(200, predictions)

        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.send_json(400, {"error": str(error)})

        except Exception:
            # Avoid exposing internal server details to the browser.
            self.send_json(500, {"error": "Prediction failed. Check the Python terminal."})

    def log_message(self, format, *args):
        print("[Web server]", format % args)


def start_site():
    server = HTTPServer(("127.0.0.1", 8000), PageHandler)

    print("Site running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    start_site()