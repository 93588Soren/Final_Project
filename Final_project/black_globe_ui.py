
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
                            <label for="rot_per">Rotation period</label>
                            <input id="rot_per" name="rot_per"
                                   type="number" step="any" required>
                        </div>

                        <div class="field">
                            <label for="e">Orbital eccentricity</label>
                            <input id="e" name="e"
                                   type="number" step="any" required>
                        </div>

                        <div class="field">
                            <label for="a">Semi-major axis</label>
                            <input id="a" name="a"
                                   type="number" step="any" required>
                        </div>

                        <div class="field">
                            <label for="i">Orbital inclination</label>
                            <input id="i" name="i"
                                   type="number" step="any" required>
                        </div>

                        <div class="field">
                            <label for="q">Perihelion distance</label>
                            <input id="q" name="q"
                                   type="number" step="any" required>
                        </div>

                        <div class="field">
                            <label for="ad">Aphelion distance</label>
                            <input id="ad" name="ad"
                                   type="number" step="any" required>
                        </div>

                        <div class="field">
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

        let angle = 0;

        function resizeCanvas() {
            const size = canvas.clientWidth;
            const pixelRatio = window.devicePixelRatio || 1;

            canvas.width = size * pixelRatio;
            canvas.height = size * pixelRatio;

            ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
        }

        function drawGlobe() {
            const size = canvas.clientWidth;
            const center = size / 2;
            const radius = size * 0.36;

            ctx.clearRect(0, 0, size, size);
            ctx.strokeStyle = "rgba(210, 210, 210, 0.42)";
            ctx.lineWidth = 0.7;

            // Latitude lines
            for (let lat = -75; lat <= 75; lat += 15) {
                const latitude = lat * Math.PI / 180;
                const y = center - Math.sin(latitude) * radius;
                const ringRadius = Math.cos(latitude) * radius;

                ctx.beginPath();
                ctx.ellipse(
                    center, y, ringRadius, ringRadius * 0.16,
                    0, 0, Math.PI * 2
                );
                ctx.stroke();
            }

            // Longitude lines
            for (let lon = 0; lon < 180; lon += 15) {
                const longitude = (lon * Math.PI / 180) + angle;

                ctx.beginPath();

                for (let step = 0; step <= 180; step++) {
                    const latitude = (step - 90) * Math.PI / 180;

                    const x =
                        center +
                        radius * Math.cos(latitude) * Math.sin(longitude);

                    const y =
                        center - radius * Math.sin(latitude);

                    if (step === 0) {
                        ctx.moveTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                }

                ctx.stroke();
            }

            angle += 0.003;
            requestAnimationFrame(drawGlobe);
        }

        resizeCanvas();
        window.addEventListener("resize", resizeCanvas);
        drawGlobe();

        // Submit asteroid data to Python
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

                result.textContent =
                    "KNN prediction: " + data.knn +
                    " | Logistic regression: " + data.logistic_regression;

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
    "rot_per",
    "e",
    "a",
    "i",
    "q",
    "ad",
    "moid_km",
]


def run_predictions(new_asteroid):
    new_asteroid = np.asarray(new_asteroid, dtype=float).reshape(-1)

    if len(new_asteroid) != len(FEATURES):
        raise ValueError("Exactly 9 asteroid measurements are required.")

    if not np.all(np.isfinite(new_asteroid)):
        raise ValueError("All measurements must be finite numbers.")

    knn_result = KNN.predict(new_asteroid)
    logistic_result = logistical_reg.predict(new_asteroid)

    # Support either a scalar or a one-element NumPy array.
    knn_result = int(np.asarray(knn_result).item())
    logistic_result = int(np.asarray(logistic_result).item())

    return {
        "knn": knn_result,
        "logistic_regression": logistic_result,
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

            # Require all nine named inputs.
            if any(name not in data for name in FEATURES):
                self.send_json(400, {"error": "Please provide all 9 measurements."})
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
