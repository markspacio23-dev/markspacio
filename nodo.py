import http.server
import socketserver
import json
import os

PORT = 9090
DIRECTORY = "hosting"

class SovereignHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "ONLINE",
                "system": "Markspacio Sovereign Core",
                "origin": "Paraguay 🇵🇾"
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            super().do_GET()

print(f"[+] Iniciando nodo soberano en puerto {PORT}...")
with socketserver.TCPServer(("", PORT), SovereignHandler) as httpd:
    httpd.serve_forever()
