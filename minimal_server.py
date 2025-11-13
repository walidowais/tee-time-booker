#!/usr/bin/env python3
"""
Minimal server for Replit debugging
Run this if main.py doesn't work
"""

import http.server
import socketserver
import json
from datetime import datetime

class TeeTimeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "online",
                "service": "Tee Time Booking Automation",
                "message": "Server is running!",
                "timestamp": datetime.now().isoformat(),
                "endpoints": {
                    "/run": "Trigger booking (not implemented in minimal server)",
                    "/status": "Check status",
                    "/health": "Health check"
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode())

        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "timestamp": datetime.now().isoformat()}
            self.wfile.write(json.dumps(response).encode())

        elif self.path == '/run':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "minimal_server",
                "message": "This is the minimal server. Use main.py for full functionality.",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())

        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = 5000
    with socketserver.TCPServer(("0.0.0.0", PORT), TeeTimeHandler) as httpd:
        print(f"🚀 Minimal server running on port {PORT}")
        print(f"📡 Visit: https://tee-time-booker.walidowais.repl.co/")
        httpd.serve_forever()
