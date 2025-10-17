"""Test file to demonstrate GitHub Models LLM failure analysis.

This test is intentionally designed to fail to trigger the AI-powered
failure analysis in the CI/CD pipeline.
"""
import pytest


@pytest.mark.llm_demo
def test_that_will_fail_for_llm_demo():
    """This test intentionally fails to demonstrate LLM analysis."""
    # Simulate a real-world failure scenario
    result = 2 + 2
    assert result == 5, (
        "Expected 2 + 2 to equal 5, but got 4. "
        "This is a demonstration test to trigger AI analysis."
    )


@pytest.mark.llm_demo
def test_network_error_simulation():
    """Simulates a network-related failure for LLM analysis."""
    # Simulate a network error
    raise ConnectionError(
        "Failed to connect to external API: timeout after 30s. "
        "This could be a flaky network issue or a real problem."
    )


@pytest.mark.llm_demo
def test_assertion_error_with_context():
    """Simulates an assertion failure with context for LLM analysis."""
    data = {"status": "error", "code": 500, "message": "Internal server error"}
    expected_status = "success"
    assert data["status"] == expected_status, (
        f"API returned error status: {data['status']} "
        f"(code: {data['code']}, message: {data['message']})"
    )
