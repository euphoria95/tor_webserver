#!/usr/bin/env python3

import logging
import http.server
import socketserver

LANDING_PAGE = """\
<html>
<head>
  <meta charset="utf-8">
  <title>Tor Hidden Service</title>
</head>
<body>
  <h1>Welcome to my .onion service!</h1>
  <p>Supported HTTP methods: GET, POST, HEAD, OPTIONS.</p>
  <p>Try a POST request with curl, for example:</p>
  <pre>curl -X POST -d "hello=world" http://YOUR_ONION_ADDRESS/ --socks5-hostname 127.0.0.1:9050</pre>
</body>
</html>
"""

class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Return a simple landing page for GET requests
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(LANDING_PAGE.encode("utf-8"))

    def do_POST(self):
        # Example POST handling: read the data and log it
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''

        logging.debug(f"Received POST data: {post_data.decode('utf-8', errors='replace')}")

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        response_text = "Thank you for the POST data!\n"
        self.wfile.write(response_text.encode("utf-8"))

    def do_HEAD(self):
        # HEAD should return the same headers as GET, but without a response body
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

    def do_OPTIONS(self):
        # Indicate which methods are allowed
        self.send_response(200)
        self.send_header("Allow", "GET,POST,HEAD,OPTIONS")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, format, *args):
        # Override default log_message to use Python's logging at DEBUG level
        logging.debug("%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args
        ))

def run_server():
    # Configure logging to show all debug messages on stdout
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    server_address = ("127.0.0.1", 80)
    with socketserver.TCPServer(server_address, CustomHandler) as httpd:
        logging.info("HTTP server is listening on %s:%d (supports GET,POST,HEAD,OPTIONS)", *server_address)
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
