"""
infrlo 静态站点服务入口
自动定位 index.html 所在目录作为站点根目录
"""
import http.server
import socketserver
import os
import sys

PORT = int(os.environ.get("PORT", 8000))
BASE = os.path.dirname(os.path.abspath(__file__))


def find_site_root(base):
    # 优先：base 自身就有 index.html
    if os.path.isfile(os.path.join(base, "index.html")):
        return base
    # 其次：base 下第一个含 index.html 的直接子目录
    for name in sorted(os.listdir(base)):
        cand = os.path.join(base, name)
        if os.path.isdir(cand) and os.path.isfile(os.path.join(cand, "index.html")):
            return cand
    return base

ROOT = find_site_root(BASE)
os.chdir(ROOT)

print("=" * 50, flush=True)
print(f"PORT      : {PORT}", flush=True)
print(f"SITE ROOT : {ROOT}", flush=True)
print(f"index.html: {os.path.isfile('index.html')}", flush=True)
print(f"files     : {sorted(os.listdir('.'))}", flush=True)
print("=" * 50, flush=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.address_string(), fmt % args))
        sys.stderr.flush()


try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Listening on 0.0.0.0:{PORT}", flush=True)
        httpd.serve_forever()
except OSError as e:
    print(f"FATAL: cannot bind port {PORT}: {e}", flush=True)
    raise
