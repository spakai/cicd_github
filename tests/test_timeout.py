"""Tests that simulate timeout scenarios - will trigger retry mechanisms."""
import time
import pytest


@pytest.mark.timeout
def test_slow_network_request():
    """Simulates a slow network request that might timeout."""
    # Simulate slow network
    time.sleep(2)
    assert True


@pytest.mark.timeout
def test_database_query_timeout():
    """Simulates a slow database query."""
    # Simulate slow DB query
    time.sleep(1.5)
    assert True


@pytest.mark.timeout
def test_external_api_timeout():
    """Simulates calling a slow external API."""
    # Simulate external API delay
    time.sleep(2.5)
    assert True


@pytest.mark.timeout
def test_file_io_timeout():
    """Simulates slow file I/O operations."""
    # Simulate slow file operations
    time.sleep(1)
    assert True


@pytest.mark.timeout
def test_computation_timeout():
    """Simulates a computationally intensive operation."""
    # Simulate heavy computation
    time.sleep(2)
    assert True