import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8000))
os.chdir(os.path.join(os.path.dirname(__file__), "web_tool"))

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()