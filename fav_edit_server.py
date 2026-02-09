#!/usr/bin/env -S uv run
"""Tiny server for the favicon editor. Serves static files + saves favicon.json."""

import http.server
import json
import os

PORT = 8032
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_POST(self):
        if self.path == '/favicon.json':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            with open(os.path.join(DIR, 'favicon.json'), 'w') as f:
                f.write('[\n')
                for i, row in enumerate(data):
                    f.write('  ' + json.dumps(row))
                    f.write(',\n' if i < len(data) - 1 else '\n')
                f.write(']\n')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'ok')
            print("Saved favicon.json")
        elif self.path == '/favicon.png':
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
            with open(os.path.join(DIR, 'favicon.png'), 'wb') as f:
                f.write(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'ok')
            print("Saved favicon.png")
        else:
            self.send_response(404)
            self.end_headers()

print(f"Favicon editor: http://localhost:{PORT}/fav_edit.html")
http.server.HTTPServer(('', PORT), Handler).serve_forever()
