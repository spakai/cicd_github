"""Minimal HTTP server exposing a Fibonacci endpoint."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from .core import fibonacci


class FibRequestHandler(BaseHTTPRequestHandler):
    """Handle GET requests for Fibonacci numbers."""

    def do_GET(self) -> None:  # pylint: disable=invalid-name
        """
        Handle HTTP GET requests for the Fibonacci endpoint.
        Parses the query string for parameter 'n', validates it,
        computes the Fibonacci number, and returns the result as JSON.
        """
        parsed = urlparse(self.path)
        if parsed.path != "/fib/":
            self.send_error(404)
            return

        params = parse_qs(parsed.query)
        if "n" not in params:
            self.send_error(400, "missing n parameter")
            return
        try:
            n = int(params["n"][0])
            value = fibonacci(n)
        except (ValueError, TypeError):
            self.send_error(
                400,
                "invalid n parameter"
            )
            return

        body = json.dumps({
            "n": n,
            "value": value
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Run the HTTP server."""
    server = HTTPServer((host, port), FibRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run(host="0.0.0.0", port=8000)
    if __name__ == "__main__":
        run(host="0.0.0.0", port=8000)
