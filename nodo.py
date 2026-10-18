import http.server, socketserver, os, json, hashlib, threading, time
from datetime import datetime

PORT = 9090
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ProfessionalEdgeHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split("?")[0]
        if path == "/" or path == "":
            return os.path.join(DIRECTORY, "hosting", "index.html")
        return os.path.join(DIRECTORY, path.lstrip("/"))

    def end_headers(self):
        self.send_header("X-Edge-Server", "Markspacio-Sovereign-Core/2.1")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def _get_directory_hash(self):
        sha256_hash = hashlib.sha256()
        for root, dirs, files in os.walk(DIRECTORY):
            for file in sorted(files):
                if file.endswith((".py", ".html", ".css", ".js", ".md")):
                    with open(os.path.join(root, file), "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            status = {
                "ecosystem": "Markspacio Professional Edge",
                "status": "ONLINE",
                "autopilot": "ACTIVE & AUTONOMOUS",
                "tier": "ENTERPRISE SOVEREIGN",
                "integrity_hash": self._get_directory_hash(),
                "active_modules": ["hosting_core", "negocios_rm/luna_rosa", "auditoria_engine", "agentes"],
                "timestamp": str(datetime.now()),
                "repository": "markspacio23-dev/markspacio"
            }
            self.wfile.write(json.dumps(status, indent=4).encode("utf-8"))
            return
        
        local_path = self.translate_path(self.path)
        if not os.path.exists(local_path) and not self.path.startswith("/api/"):
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<!DOCTYPE html><html><body style=\"background:#030712;color:#f472b6;font-family:monospace;text-align:center;padding-top:100px;\"><h1>404 - RECURSO NO ENCONTRADO</h1><p>Nodo Soberano Markspacio</p></body></html>")
            return

        return super().do_GET()

def run_autopilot():
    while True:
        time.sleep(30)

print("[+] Iniciando Motor de Hosting Profesional al Borde...")
threading.Thread(target=run_autopilot, daemon=True).start()

with socketserver.TCPServer(("", PORT), ProfessionalEdgeHandler) as httpd:
    print(f"[+] Nodo escuchando en puerto {PORT}...")
    httpd.serve_forever()
