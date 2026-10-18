import http.server, socketserver, os
PORT = 9090
DIR = os.path.expanduser("~/nube_soberana")
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("==========================================")
    print("🚀 NODO SOBERANO FUNCIONAL ACTIVO")
    print("📡 Escuchando en http://127.0.0.1:9090")
    print("==========================================")
    httpd.serve_forever()
