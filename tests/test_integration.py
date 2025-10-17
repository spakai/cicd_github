"""Integration tests that demonstrate ML-powered test selection."""
import pytest


class TestFibonacciIntegration:
    """Integration tests for Fibonacci calculations."""

    def test_fibonacci_sequence_integration(self):
        """Tests the full Fibonacci sequence calculation."""
        from fib.core import fibonacci
        sequence = [fibonacci(n) for n in range(15)]
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
        assert sequence == expected

    def test_fibonacci_large_numbers(self):
        """Tests Fibonacci with large numbers."""
        from fib.core import fibonacci
        assert fibonacci(20) == 6765
        assert fibonacci(25) == 75025

    def test_fibonacci_edge_cases(self):
        """Tests Fibonacci edge cases."""
        from fib.core import fibonacci
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
        assert fibonacci(2) == 1


class TestAPIIntegration:
    """Integration tests for the API."""

    def test_api_endpoint_integration(self):
        """Tests API endpoint with various inputs."""
        from fib.api import FibRequestHandler
        from http.server import HTTPServer
        from threading import Thread
        import json
        import urllib.request

        server = HTTPServer(("127.0.0.1", 0), FibRequestHandler)
        thread = Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        try:
            # Test multiple requests
            for n in [5, 10, 15]:
                url = (f"http://{server.server_name}:"
                       f"{server.server_port}/fib/?n={n}")
                with urllib.request.urlopen(url) as resp:
                    data = json.loads(resp.read().decode())
                    assert data["n"] == n
        finally:
            server.shutdown()
            thread.join(timeout=1.0)

    def test_api_error_handling(self):
        """Tests API error handling."""
        from fib.api import FibRequestHandler
        from http.server import HTTPServer
        from threading import Thread
        import urllib.error

        server = HTTPServer(("127.0.0.1", 0), FibRequestHandler)
        thread = Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()  # FIXED: Start the thread!

        try:
            url = (f"http://{server.server_name}:"
                   f"{server.server_port}/fib/?n=-5")
            with pytest.raises(urllib.error.HTTPError):
                urllib.request.urlopen(url)
        finally:
            server.shutdown()
            thread.join(timeout=1.0)  # Add timeout to prevent hanging


class TestPerformanceIntegration:
    """Performance-related integration tests."""

    def test_fibonacci_performance(self):
        """Tests that Fibonacci calculation is performant."""
        import time
        from fib.core import fibonacci

        start = time.time()
        result = fibonacci(30)
        elapsed = time.time() - start

        assert result == 832040
        assert elapsed < 1.0  # Should complete in under 1 second

    def test_concurrent_api_requests(self):
        """Tests handling concurrent API requests."""
        from fib.api import FibRequestHandler
        from http.server import HTTPServer
        from threading import Thread
        import urllib.request

        server = HTTPServer(("127.0.0.1", 0), FibRequestHandler)
        thread = Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        try:
            # Make concurrent requests
            import concurrent.futures
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
            with executor:
                futures = []
                for n in range(10, 15):
                    url = (f"http://{server.server_name}:"
                           f"{server.server_port}/fib/?n={n}")
                    future = executor.submit(
                        lambda u: urllib.request.urlopen(u).read(), url
                    )
                    futures.append(future)

                # Wait for all requests to complete
                results = [f.result() for f in futures]
                assert len(results) == 5
        finally:
            server.shutdown()
            thread.join(timeout=1.0)
