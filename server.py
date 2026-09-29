from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs
from supplement_fixture.local import read_local
from supplement_fixture.cached import read_cached
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        request = urlsplit(self.path)
        if request.path == "/health":
            self.send_response(200); self.end_headers(); self.wfile.write(b"owned-service-ok\n"); return
        name = parse_qs(request.query).get("name", ["hello.txt"])[0]
        try:
            content = read_cached(name) if request.path == "/cached" else read_local(os.environ.get("FIXTURE_LOCAL_ROOT", "/data/documents"), name)
            self.send_response(200); self.end_headers(); self.wfile.write(content.encode())
        except Exception:
            self.send_response(503); self.end_headers(); self.wfile.write(b"optional fixture unavailable\n")

if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
