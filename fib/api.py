"""Minimal HTTP server exposing a Fibonacci endpoint."""

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from .core import fibonacci, fibonacci_sequence


class FibRequestHandler(BaseHTTPRequestHandler):
    """Handle GET requests for Fibonacci numbers."""

    def do_GET(self) -> None:  # pylint: disable=invalid-name
        """
        Handle HTTP GET requests for the Fibonacci endpoint.
        Parses the query string for parameter 'n', validates it,
        computes the Fibonacci number, and returns the result as JSON.
        """
        parsed = urlparse(self.path)
        if parsed.path == "/fib/":
            self._handle_single_value(parsed)
            return
        if parsed.path == "/fib/sequence/":
            self._handle_sequence(parsed)
            return

        self.send_error(404)

    def _handle_single_value(self, parsed) -> None:
        params = parse_qs(parsed.query)
        if "n" not in params:
            self.send_error(400, "missing n parameter")
            return
        try:
            n = int(params["n"][0])
            value = fibonacci(n)
        except (ValueError, TypeError):
            self.send_error(400, "invalid n parameter")
            return

        self._write_json({"n": n, "value": value})

    def _handle_sequence(self, parsed) -> None:
        params = parse_qs(parsed.query)
        if "count" not in params:
            self.send_error(400, "missing count parameter")
            return
        try:
            count = int(params["count"][0])
            sequence = fibonacci_sequence(count)
        except (ValueError, TypeError):
            self.send_error(400, "invalid count parameter")
            return

        self._write_json({"count": count, "sequence": sequence})

    def _write_json(self, payload: dict) -> None:
        body = json.dumps(payload).encode()
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
    default_port = os.getenv("FIB_SERVER_PORT", "8000")
    try:
        configured_port = int(default_port)
    except ValueError:
        raise ValueError("FIB_SERVER_PORT must be an integer") from None

    run(host=os.getenv("FIB_SERVER_HOST", "127.0.0.1"), port=configured_port)
