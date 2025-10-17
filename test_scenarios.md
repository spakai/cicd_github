# Test Scenarios for Self-Healing CI/CD

This document describes the test scenarios that demonstrate the intelligent features of the CI/CD pipeline.

## ⚡ Quick Reference

| Scenario | Markers / Files | Command |
| --- | --- | --- |
| Flaky auto-retry | `pytest -m flaky` / `tests/test_flaky.py` | `./trigger_scenarios.sh flaky` |
| Timeout handling | `pytest -m timeout` / `tests/test_timeout.py` | `./trigger_scenarios.sh timeout` |
| ML-powered selection | `pytest -m "ml_critical or ml_high_risk"` / `tests/test_ml_features.py` | `./trigger_scenarios.sh ml-critical` |
| Integration coverage | `pytest tests/test_integration.py` | `./trigger_scenarios.sh integration` |

## 🧪 Flaky Test Scenarios (Auto-Retry)

The following tests in `test_flaky.py` simulate real-world flaky behavior:

### 1. Network Flakiness
- **Test**: `test_flaky_network_call()`
- **Failure Rate**: 30%
- **Trigger**: ConnectionError with "Network is unreachable"
- **Self-Healing**: Auto-retry with 2 attempts and 3-second delay
- **Expected Behavior**: Pipeline will automatically retry and likely pass on second attempt

### 2. Database Connection Flakiness
- **Test**: `test_flaky_database_connection()`
- **Failure Rate**: 25%
- **Trigger**: TimeoutError for database connection
- **Self-Healing**: Auto-retry mechanism
- **Expected Behavior**: Retry will handle temporary DB connection issues

### 3. External Service Flakiness
- **Test**: `test_flaky_external_service()`
- **Failure Rate**: 20%
- **Trigger**: Generic exception for service unavailability
- **Self-Healing**: Auto-retry with delays
- **Expected Behavior**: Pipeline recovers from external service hiccups

### 4. Timing-Dependent Failures
- **Test**: `test_flaky_assertion()`
- **Failure Rate**: 15%
- **Trigger**: Race condition or timing issue
- **Self-Healing**: Retry with delays helps resolve timing issues
- **Expected Behavior**: Delays between retries help timing-dependent tests pass

### 5. Resource Contention
- **Test**: `test_flaky_resource_lock()`
- **Failure Rate**: 20%
- **Trigger**: Resource lock acquisition failure
- **Self-Healing**: Retry mechanism
- **Expected Behavior**: Retry allows resource to become available

## ⏱️ Timeout Scenarios

The following tests in `test_timeout.py` simulate slow operations:

### 1. Slow Network Requests
- **Test**: `test_slow_network_request()`
- **Duration**: 2 seconds
- **Trigger**: Simulates slow network response
- **Self-Healing**: If timeout occurs, auto-retry will be triggered
- **Expected Behavior**: Pipeline handles slow network gracefully

### 2. Database Query Timeouts
- **Test**: `test_database_query_timeout()`
- **Duration**: 1.5 seconds
- **Trigger**: Simulates slow database query
- **Self-Healing**: Retry on timeout
- **Expected Behavior**: Pipeline recovers from slow DB queries

### 3. External API Timeouts
- **Test**: `test_external_api_timeout()`
- **Duration**: 2.5 seconds
- **Trigger**: Simulates slow external API
- **Self-Healing**: Auto-retry mechanism
- **Expected Behavior**: Pipeline handles slow external services

### 4. File I/O Timeouts
- **Test**: `test_file_io_timeout()`
- **Duration**: 1 second
- **Trigger**: Simulates slow file operations
- **Self-Healing**: Retry on timeout
- **Expected Behavior**: Pipeline handles slow I/O operations

### 5. Computation Timeouts
- **Test**: `test_computation_timeout()`
- **Duration**: 2 seconds
- **Trigger**: Simulates heavy computation
- **Self-Healing**: Retry mechanism
- **Expected Behavior**: Pipeline handles computationally intensive operations

## 🤖 ML-Powered Test Selection Scenarios

The following tests in `test_ml_features.py` demonstrate intelligent test selection:

### 1. Critical Path Tests (Always Run)
- **Marker**: `@pytest.mark.ml_critical`
- **Tests**: Core business logic and critical API endpoints
- **Expected Behavior**: ML will always select these tests
- **Example**: `test_critical_business_logic()`, `test_critical_api_endpoint()`

### 2. Affected Tests (Selective Run)
- **Marker**: `@pytest.mark.ml_affected`
- **Tests**: Recently modified features and dependent modules
- **Expected Behavior**: ML identifies and runs only affected tests
- **Example**: `test_recently_modified_feature()`, `test_dependent_module()`

### 3. High-Risk Area Tests (Priority Run)
- **Marker**: `@pytest.mark.ml_high_risk`
- **Tests**: Edge cases and boundary conditions
- **Expected Behavior**: ML prioritizes these tests
- **Example**: `test_edge_case_handling()`, `test_boundary_conditions()`

### 4. Low-Priority Tests (Can Skip)
- **Marker**: `@pytest.mark.ml_low_priority`
- **Tests**: Rarely failing optimizations and legacy code
- **Expected Behavior**: ML can safely skip these tests
- **Example**: `test_rarely_failing_optimization()`, `test_legacy_code_path()`

### 5. Experimental Feature Tests (Optional)
- **Marker**: `@pytest.mark.ml_experimental`
- **Tests**: New alpha and beta features
- **Expected Behavior**: ML may skip these for faster CI
- **Example**: `test_new_feature_alpha()`, `test_beta_feature()`

## 🔍 Integration Test Scenarios

The following tests in `test_integration.py` demonstrate comprehensive testing:

### 1. Full Sequence Integration
- **Test**: `test_fibonacci_sequence_integration()`
- **Purpose**: Tests complete Fibonacci sequence calculation
- **Expected Behavior**: Validates end-to-end functionality

### 2. Large Number Handling
- **Test**: `test_fibonacci_large_numbers()`
- **Purpose**: Tests performance with large inputs
- **Expected Behavior**: Validates scalability

### 3. Edge Case Integration
- **Test**: `test_fibonacci_edge_cases()`
- **Purpose**: Tests boundary conditions
- **Expected Behavior**: Validates robustness

### 4. API Endpoint Integration
- **Test**: `test_api_endpoint_integration()`
- **Purpose**: Tests API with various inputs
- **Expected Behavior**: Validates API functionality

### 5. Error Handling Integration
- **Test**: `test_api_error_handling()`
- **Purpose**: Tests error scenarios
- **Expected Behavior**: Validates error handling

### 6. Performance Integration
- **Test**: `test_fibonacci_performance()`
- **Purpose**: Tests performance requirements
- **Expected Behavior**: Validates performance

### 7. Concurrent Requests
- **Test**: `test_concurrent_api_requests()`
- **Purpose**: Tests concurrent handling
- **Expected Behavior**: Validates concurrency

## 🎯 How to Trigger Each Scenario

### Trigger Flaky Tests
```bash
# Run only flaky tests
pytest -m flaky

# Run with retry configuration
pytest -m flaky --reruns 2 --reruns-delay 3
```

### Trigger Timeout Tests
```bash
# Run only timeout tests
pytest -m timeout

# Run with timeout configuration
pytest -m timeout --timeout=30
```

### Trigger ML-Critical Tests
```bash
# Run only critical tests
pytest -m ml_critical

# Run critical and high-risk tests
pytest -m "ml_critical or ml_high_risk"
```

### Trigger Integration Tests
```bash
# Run integration tests
pytest tests/test_integration.py

# Run with coverage
pytest tests/test_integration.py --cov=fib
```

## 📊 Expected CI/CD Behavior

### Scenario 1: Flaky Test Failure
1. Test fails due to network flakiness
2. Pipeline detects failure and classifies it
3. Self-healing mechanism kicks in
4. Test is automatically retried with delay
5. Test passes on retry
6. Pipeline continues successfully

### Scenario 2: Timeout Failure
1. Test times out after 30 seconds
2. Pipeline detects timeout
3. Failure is classified as timeout issue
4. Auto-remedy retries the test
5. Test completes within timeout on retry
6. Pipeline continues successfully

### Scenario 3: ML Test Selection
1. PR is created with code changes
2. Launchable analyzes changed code
3. ML selects only affected tests
4. Pipeline runs subset of tests
5. CI completes faster
6. Full test suite runs on merge

### Scenario 4: AI Failure Analysis
1. Test fails with unknown error
2. Pipeline classifies failure
3. GitHub Models analyzes logs
4. AI provides summary and suggestions
5. Summary is posted to PR
6. Developer gets actionable insights

## 🚀 Best Practices

1. **Mark flaky tests** with `@pytest.mark.flaky` for auto-retry
2. **Mark critical tests** with `@pytest.mark.ml_critical` for ML selection
3. **Use appropriate timeouts** for slow operations
4. **Categorize tests** by risk and priority
5. **Monitor retry rates** to identify truly flaky tests
6. **Review AI summaries** to improve test reliability

