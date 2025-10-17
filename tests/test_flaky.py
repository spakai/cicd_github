"""Tests that simulate flaky behavior - will trigger auto-retry mechanisms."""
import random
import pytest


@pytest.mark.flaky
def test_flaky_network_call():
    """Simulates a flaky network call that fails 40% of the time."""
    # Simulate network flakiness - high failure rate to test retries
    if random.random() < 0.4:
        raise ConnectionError("Network is unreachable - temporary failure")
    assert True


@pytest.mark.flaky
def test_flaky_database_connection():
    """Simulates a flaky database connection."""
    # Simulate DB connection timeout - high failure rate to test retries
    if random.random() < 0.4:
        raise TimeoutError("Database connection timed out")
    assert True


@pytest.mark.flaky
def test_flaky_external_service():
    """Simulates calling an external service that occasionally fails."""
    # Simulate external service failure - high failure rate to test retries
    if random.random() < 0.4:
        raise Exception("External service temporarily unavailable")
    assert True


@pytest.mark.flaky
def test_flaky_assertion():
    """Simulates a flaky assertion that sometimes fails."""
    # Simulate race condition or timing issue - high failure rate to test retries
    import time
    time.sleep(0.01)
    if random.random() < 0.4:
        assert False, "Timing-dependent assertion failed"
    assert True


@pytest.mark.flaky
def test_flaky_resource_lock():
    """Simulates a flaky resource lock that occasionally fails."""
    # Simulate resource contention - high failure rate to test retries
    if random.random() < 0.4:
        raise RuntimeError("Resource lock acquisition failed")
    assert True
