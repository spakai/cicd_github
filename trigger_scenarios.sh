#!/bin/bash
# Script to trigger different test scenarios for demonstrating self-healing CI/CD

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Test Scenario Trigger Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest is not installed. Please install it first:"
    echo "   pip install pytest pytest-cov pytest-rerunfailures"
    exit 1
fi

# Function to run tests with retry
run_with_retry() {
    local test_args="$1"
    local description="$2"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Scenario: $description"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    pytest $test_args || {
        echo ""
        echo "⚠️  Test run completed with some failures (this is expected for flaky tests)"
        echo "   Self-healing mechanisms should have retried failed tests"
    }
    
    echo ""
    echo "✅ Scenario complete"
    echo ""
}

# Parse command line arguments
SCENARIO=${1:-all}

case $SCENARIO in
    flaky)
        echo "🎯 Running FLACKY TEST scenarios"
        echo "   These tests simulate network/database/external service flakiness"
        echo "   Expected: Some tests may fail initially, then pass on retry"
        echo ""
        run_with_retry "-m flaky --reruns 2 --reruns-delay 3 -v" "Flaky Tests (Auto-Retry)"
        ;;
    
    timeout)
        echo "🎯 Running TIMEOUT scenarios"
        echo "   These tests simulate slow operations"
        echo "   Expected: Tests should complete within timeout"
        echo ""
        run_with_retry "-m timeout --timeout=30 -v" "Timeout Tests"
        ;;
    
    ml-critical)
        echo "🎯 Running ML-CRITICAL scenarios"
        echo "   These tests should always be selected by ML"
        echo "   Expected: All critical tests run"
        echo ""
        run_with_retry "-m ml_critical -v" "ML Critical Tests"
        ;;
    
    ml-affected)
        echo "🎯 Running ML-AFFECTED scenarios"
        echo "   These tests simulate affected by recent changes"
        echo "   Expected: Only affected tests run"
        echo ""
        run_with_retry "-m ml_affected -v" "ML Affected Tests"
        ;;
    
    ml-high-risk)
        echo "🎯 Running ML-HIGH-RISK scenarios"
        echo "   These tests are in high-risk areas"
        echo "   Expected: High-risk tests run with priority"
        echo ""
        run_with_retry "-m ml_high_risk -v" "ML High-Risk Tests"
        ;;
    
    integration)
        echo "🎯 Running INTEGRATION scenarios"
        echo "   These tests validate end-to-end functionality"
        echo "   Expected: All integration tests pass"
        echo ""
        run_with_retry "tests/test_integration.py -v" "Integration Tests"
        ;;
    
    all)
        echo "🎯 Running ALL scenarios"
        echo "   This will demonstrate all self-healing features"
        echo ""
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Step 1: Running Core Tests"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        pytest tests/test_core.py tests/test_api.py -v
        echo ""
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Step 2: Running Flaky Tests (with auto-retry)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        pytest -m flaky --reruns 2 --reruns-delay 3 -v || echo "⚠️  Some flaky tests failed (expected)"
        echo ""
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Step 3: Running Timeout Tests"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        pytest -m timeout --timeout=30 -v
        echo ""
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Step 4: Running ML-Critical Tests"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        pytest -m ml_critical -v
        echo ""
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Step 5: Running Integration Tests"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        pytest tests/test_integration.py -v
        echo ""
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "✅ All scenarios complete!"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ;;
    
    *)
        echo "❌ Unknown scenario: $SCENARIO"
        echo ""
        echo "Usage: $0 [scenario]"
        echo ""
        echo "Available scenarios:"
        echo "  flaky         - Run flaky tests with auto-retry"
        echo "  timeout       - Run timeout tests"
        echo "  ml-critical   - Run ML-critical tests"
        echo "  ml-affected   - Run ML-affected tests"
        echo "  ml-high-risk  - Run ML-high-risk tests"
        echo "  integration   - Run integration tests"
        echo "  all           - Run all scenarios (default)"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Test Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To see self-healing in action in CI/CD:"
echo "  1. Push these changes to GitHub"
echo "  2. Create a Pull Request"
echo "  3. Watch the CI/CD pipeline run"
echo "  4. Observe the self-healing mechanisms in action"
echo ""
echo "For more details, see: test_scenarios.md"
echo ""

