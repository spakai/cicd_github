"""Tests specifically designed to demonstrate ML-powered test selection."""
import pytest


@pytest.mark.ml_critical
class TestMLCriticalPath:
    """Critical path tests that ML should always select."""

    def test_critical_business_logic(self):
        """Tests the most critical business logic."""
        from fib.core import fibonacci
        # This is the core business logic that should always be tested
        assert fibonacci(10) == 55

    def test_critical_api_endpoint(self):
        """Tests the most critical API endpoint."""
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
            url = f"http://{server.server_name}:{server.server_port}/fib/?n=10"
            with urllib.request.urlopen(url) as resp:
                data = json.loads(resp.read().decode())
                assert data == {"n": 10, "value": 55}
        finally:
            server.shutdown()
            thread.join(timeout=1.0)


@pytest.mark.ml_affected
class TestMLAffectedByChanges:
    """Tests that ML identifies as affected by recent changes."""

    def test_recently_modified_feature(self):
        """Simulates a test for a recently modified feature."""
        from fib.core import fibonacci
        # This would be a test for recently changed code
        assert fibonacci(5) == 5

    def test_dependent_module(self):
        """Simulates a test for a module that depends on changed code."""
        from fib.core import fibonacci
        # This module depends on recently changed code
        result = fibonacci(7)
        assert result == 13


@pytest.mark.ml_high_risk
class TestMLHighRiskAreas:
    """Tests in high-risk areas that ML should prioritize."""

    def test_edge_case_handling(self):
        """Tests edge case handling in high-risk areas."""
        from fib.core import fibonacci
        with pytest.raises(ValueError):
            fibonacci(-1)

    def test_boundary_conditions(self):
        """Tests boundary conditions."""
        from fib.core import fibonacci
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1


@pytest.mark.ml_low_priority
class TestMLLowPriority:
    """Tests that ML can safely skip."""

    def test_rarely_failing_optimization(self):
        """Tests an optimization that rarely fails."""
        from fib.core import fibonacci
        # This test rarely fails and can be skipped by ML
        assert fibonacci(3) == 2

    def test_legacy_code_path(self):
        """Tests legacy code that hasn't changed in months."""
        from fib.core import fibonacci
        # This is legacy code, low priority for ML
        assert fibonacci(4) == 3

    def test_non_critical_feature(self):
        """Tests a non-critical feature."""
        from fib.core import fibonacci
        # Non-critical feature, can be skipped by ML
        assert fibonacci(6) == 8


@pytest.mark.ml_experimental
class TestMLExperimentalFeatures:
    """Tests for experimental features."""

    def test_new_feature_alpha(self):
        """Tests a new alpha feature."""
        from fib.core import fibonacci
        # New experimental feature
        assert fibonacci(8) == 21

    def test_beta_feature(self):
        """Tests a beta feature."""
        from fib.core import fibonacci
        # Beta feature
        assert fibonacci(9) == 34
