import http.server, socketserver, json, time, os, sqlite3
import traceback

PORT = 9090
START_TIME = time.time()
DB_FILE = "node_metrics.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, client_ip TEXT, path TEXT)")
    conn.commit()
    conn.close()

init_db()

def log_request(ip, path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO requests (timestamp, client_ip, path) VALUES (datetime('now'), ?, ?)", (ip, path))
    conn.commit()
    conn.close()

html_content = """
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markspacio - Soberano AI Core</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 2.5rem; border-radius: 16px; text-align: center; border: 1px solid #334155; box-shadow: 0 20px 25px rgba(0,0,0,0.5); max-width: 460px; width: 100%; }
        h1 { color: #38bdf8; font-size: 1.5rem; margin-bottom: 0.5rem; }
        p { color: #94a3b8; font-size: 0.90rem; margin-bottom: 1.2rem; }
        .badge { display: inline-block; background: #0369a1; color: #e0f2fe; padding: 0.3rem 0.8rem; border-radius: 9999px; font-weight: 600; font-size: 0.80rem; margin-bottom: 1rem; }
        .metrics { background: #0f172a; padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 0.80rem; color: #34d399; text-align: left; border: 1px solid #334155; margin-bottom: 1rem; }
    input, button { width: 100%; padding: 0.6rem; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: #fff; box-sizing: border-box; font-size: 0.9rem; margin-top: 0.5rem; }
        button { background: #0284c7; font-weight: bold; cursor: pointer; border: none; }
        button:hover { background: #0369a1; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Markspacio AI Core</h1>
        <p>Inferencia Soberana al Borde (Paraguay 🇵🇾)</p>
        <div class="badge">Motor Local Activo</div>
        <div class="metrics" id="metrics">Cargando telemetría...</div>
        <input type="text" id="prompt" placeholder="Escribe un prompt para la IA...">
        <button onclick="sendAI()">Ejecutar Inferencia</button>
    </div>
    <script>
        async function fetchStatus() {
            try {
                let res = await fetch("/api/status");
                let data = await res.json();
                document.getElementById("metrics").innerHTML = "> Estado: " + data.status + "<br>> Uptime: " + Math.floor(data.uptime) + "s<br>> Peticiones DB: " + data.total_requests;
            } catch(e) {
                document.getElementById("metrics").innerText = "Error de enlace";
            }
        }
        async function sendAI() {
            let promptText = document.getElementById("prompt").value;
            document.getElementById("metrics").innerText = "> Procesando IA local...";
            let res = await fetch("/api/ai", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({prompt: promptText})
            });
            let data = await res.json();
            document.getElementById("metrics").innerHTML = "Respuesta:<br>" + data.response;
        }
        fetchStatus();
        setInterval(fetchStatus, 4000);
    </script>
</body>
</html>
"""

class SovereignHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        log_request(client_ip, self.path)
        if self.path in ["/api/status", "/api/status/"]:
            uptime = time.time() - START_TIME
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM requests")
            total_reqs = cursor.fetchone()[0]
            conn.close()
            data = {
                "status": "ONLINE",
                "system": "Markspacio Sovereign Core",
                "origin": "Paraguay 🇵🇾",
                "uptime": uptime,
                "total_requests": total_reqs
            }
            body = json.dumps(data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            body = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def do_POST(self):
        client_ip = self.client_address[0]
        log_request(client_ip, self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        if self.path in ["/api/ai", "/api/ai/"]:
            try:
                req_json = json.loads(post_data.decode("utf-8"))
                prompt = req_json.get("prompt", "")
                ai_response = f"[Sovereign Core Inference] Procesado localmente en Paraguay 🇵🇾 para el prompt: '{prompt}'"
                data = {"status": "SUCCESS", "response": ai_response}
            except Exception as e:
                data = {"status": "ERROR", "response": str(e)}
            body = json.dumps(data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", PORT), SovereignHandler) as httpd:
            print(f"[+] Nodo Soberano con AI Bridge activo en el puerto {PORT}...")
            httpd.serve_forever()
    except Exception as e:
        print("[-] Error fatal en el servidor:")
        traceback.print_exc()
