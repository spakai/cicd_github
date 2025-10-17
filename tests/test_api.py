"""Tests for the Fibonacci HTTP API."""
from threading import Thread
from http.server import HTTPServer
import json
import urllib.request
import urllib.error
from fib.api import FibRequestHandler


def start_server() -> tuple[HTTPServer, Thread]:
    """Start the HTTP server in a background thread."""
    server = HTTPServer(("127.0.0.1", 0), FibRequestHandler)
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server, thread


def stop_server(server: HTTPServer, thread: Thread) -> None:
    server.shutdown()
    thread.join()


def test_get_fibonacci() -> None:
    server, thread = start_server()
    url = f"http://{server.server_name}:{server.server_port}/fib/?n=10"
    try:
        with urllib.request.urlopen(url) as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode())
            assert data == {"n": 10, "value": 55}
    finally:
        stop_server(server, thread)


def test_get_fibonacci_negative() -> None:
    server, thread = start_server()
    url = f"http://{server.server_name}:{server.server_port}/fib/?n=-1"
    try:
        with urllib.request.urlopen(url):
            # Should raise HTTPError for status >=400
            pass
    except urllib.error.HTTPError as err:
        assert err.code == 400
    finally:
        stop_server(server, thread)


def test_get_fibonacci_sequence() -> None:
    server, thread = start_server()
    url = (
        f"http://{server.server_name}:{server.server_port}/fib/sequence/?count=5"
    )
    try:
        with urllib.request.urlopen(url) as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode())
            assert data == {"count": 5, "sequence": [0, 1, 1, 2, 3]}
    finally:
        stop_server(server, thread)


def test_get_fibonacci_sequence_invalid() -> None:
    server, thread = start_server()
    url = (
        f"http://{server.server_name}:{server.server_port}/fib/sequence/?count=-1"
    )
    try:
        with urllib.request.urlopen(url):
            pass
    except urllib.error.HTTPError as err:
        assert err.code == 400
    finally:
        stop_server(server, thread)
