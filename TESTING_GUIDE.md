# Testing Guide for Self-Healing CI/CD

This guide explains how to use the test scenarios to demonstrate the intelligent features of the CI/CD pipeline.

## 🎯 Quick Start

Before running any scenario, install the Python dependencies from `requirements.txt`, activate your
virtual environment, and ensure the helper script is executable:

```bash
pip install -r requirements.txt
source venv/bin/activate  # or your preferred environment
chmod +x trigger_scenarios.sh
```

All commands below assume you are in the repository root.

### Run All Test Scenarios Locally

```bash
./trigger_scenarios.sh all
```

### Run Specific Scenarios

```bash
# Flaky tests with auto-retry
./trigger_scenarios.sh flaky

# Timeout tests
./trigger_scenarios.sh timeout

# ML-critical tests
./trigger_scenarios.sh ml-critical

# Integration tests
./trigger_scenarios.sh integration
```

## 🧪 Test Files Overview

### 1. `test_flaky.py` - Flaky Test Scenarios
Simulates real-world flaky behavior that triggers auto-retry mechanisms:
- **Network flakiness** (30% failure rate)
- **Database connection issues** (25% failure rate)
- **External service failures** (20% failure rate)
- **Timing-dependent failures** (15% failure rate)
- **Resource contention** (20% failure rate)

**How it works**: Tests randomly fail based on probability, simulating real-world flakiness. The self-healing mechanism automatically retries these tests.

**Expected behavior**: Tests may fail on first run, then pass on retry.

### 2. `test_timeout.py` - Timeout Scenarios
Simulates slow operations that might timeout:
- Slow network requests (2s)
- Database query timeouts (1.5s)
- External API timeouts (2.5s)
- File I/O timeouts (1s)
- Computation timeouts (2s)

**How it works**: Tests include intentional delays to simulate slow operations.

**Expected behavior**: Tests complete within the configured timeout.

### 3. `test_ml_features.py` - ML-Powered Test Selection
Demonstrates intelligent test selection:
- **ml_critical**: Always run these tests
- **ml_affected**: Run when code is affected
- **ml_high_risk**: High priority tests
- **ml_low_priority**: Can be safely skipped
- **ml_experimental**: Optional tests

**How it works**: Tests are marked with categories that ML can use to intelligently select which tests to run.

**Expected behavior**: ML selects only relevant tests based on code changes. To simulate this
behaviour locally, combine markers when calling `pytest`:

```bash
pytest -m "ml_critical or ml_high_risk"
```

### 4. `test_integration.py` - Integration Tests
Comprehensive end-to-end tests:
- Full sequence integration
- Large number handling
- Edge case validation
- API endpoint integration
- Error handling
- Performance validation
- Concurrent request handling

**How it works**: Tests validate complete functionality across components.

**Expected behavior**: All integration tests pass.

## 🔍 How Self-Healing Works

### Scenario 1: Flaky Network Test

```python
def test_flaky_network_call():
    if random.random() < 0.3:
        raise ConnectionError("Network is unreachable")
    assert True
```

**In CI/CD**:
1. Test runs and randomly fails with ConnectionError
2. Pipeline detects failure
3. Failure classifier identifies it as network issue
4. Auto-remedy retries the test with 3-second delay
5. Test passes on retry
6. Pipeline continues successfully

**What you'll see in logs**:
```
🔍 Self-healing: Analyzing failure...
   ⚡ Detected: Network/Timeout issue
   🔧 Action: Will retry last failed tests
🔄 Self-healing: Retrying failed tests (attempt 1/2)...
✅ Test passed on retry
```

### Scenario 2: ML Test Selection

```python
@pytest.mark.ml_critical
def test_critical_business_logic():
    assert fibonacci(10) == 55
```

**In CI/CD**:
1. Code change is detected
2. Launchable analyzes the change
3. ML identifies affected tests
4. Only relevant tests are run
5. CI completes faster

**What you'll see in logs**:
```
🤖 ML-powered test selection: Running only affected tests
   Test subset: 15 tests selected
```

### Scenario 3: AI Failure Analysis

When a test fails:
1. Pipeline extracts error logs
2. GitHub Models analyzes the failure
3. AI provides summary and suggestions
4. Summary is posted to PR

**What you'll see in PR**:
```
🤖 CI Triage (LLM):

• Detected: Flaky network test
• Root cause: Temporary network connectivity issue
• Suggested fix: Add retry logic or increase timeout
• Recommendation: This is a known flaky test, can be ignored
```

## 📚 Additional Resources

- `test_scenarios.md` – detailed descriptions of every scenario and the individual tests involved.
- `SELF_HEALING_FEATURES.md` – high-level overview of the intelligent CI/CD capabilities on display.
- `README.md` – setup instructions, CI/CD pipeline summary, and links to related documentation.

## 🚀 Demonstrating Features

### To Demonstrate Flaky Test Handling

1. **Run flaky tests locally**:
   ```bash
   ./trigger_scenarios.sh flaky
   ```

2. **Push to GitHub**:
   ```bash
   git add tests/test_flaky.py
   git commit -m "Add flaky test scenarios"
   git push
   ```

3. **Watch CI/CD**:
   - Tests may fail initially
   - Auto-retry kicks in
   - Tests pass on retry
   - Pipeline succeeds

### To Demonstrate ML Test Selection

1. **Enable Launchable** (in `ci.yml`):
   ```yaml
   USE_LAUNCHABLE: "true"
   ```

2. **Add Launchable token** (GitHub Secrets):
   - Add `LAUNCHABLE_TOKEN` secret

3. **Create a PR**:
   - Make a small code change
   - ML will select only affected tests

4. **Watch CI/CD**:
   - See "ML-powered test selection" message
   - Only relevant tests run
   - Faster CI completion

### To Demonstrate AI Failure Analysis

1. **Enable GitHub Models** (in `ci.yml`):
   ```yaml
   USE_MODELS_SUMMARY: "true"
   ```

2. **Enable GitHub Models** in repo settings:
   - Go to Settings > Security & analysis
   - Enable GitHub Models

3. **Introduce a test failure**:
   ```bash
   # Temporarily break a test
   git commit --allow-empty -m "Trigger failure"
   git push
   ```

4. **Watch CI/CD**:
   - Test fails
   - AI analyzes failure
   - Summary posted to PR
   - Actionable insights provided

## 📊 Monitoring Self-Healing

### Check Retry Statistics

In CI/CD logs, look for:
```
🧪 Self-healing: Auto-retry enabled (2 retries with 3s delay)
🔄 Self-healing: Retrying failed tests (attempt 1/2)...
```

### Check ML Test Selection

In CI/CD logs, look for:
```
🤖 ML-powered test selection: Running only affected tests
   Test subset: 15 tests selected
```

### Check AI Analysis

In PR comments, look for:
```
🤖 CI Triage (LLM):
[AI-generated summary]
```

## 🎓 Best Practices

### 1. Mark Flaky Tests

Always mark flaky tests with `@pytest.mark.flaky`:
```python
@pytest.mark.flaky
def test_external_api():
    # This test is known to be flaky
    pass
```

### 2. Use Appropriate Timeouts

Set timeouts for slow operations:
```python
@pytest.mark.timeout
def test_slow_operation():
    # This test may take time
    pass
```

### 3. Categorize Tests for ML

Use markers to help ML select tests:
```python
@pytest.mark.ml_critical
def test_core_functionality():
    # Always run this test
    pass

@pytest.mark.ml_low_priority
def test_rarely_failing():
    # Can be skipped by ML
    pass
```

### 4. Monitor Retry Rates

Track which tests are being retried:
- High retry rate = truly flaky test
- Low retry rate = occasional network issues
- Zero retry rate = stable test

### 5. Review AI Summaries

Use AI-generated summaries to:
- Identify patterns in failures
- Prioritize fixes
- Improve test reliability

## 🔧 Troubleshooting

### Tests Not Retrying

**Problem**: Flaky tests fail but don't retry.

**Solution**: Check that `USE_RERUNS` is set to `"true"` in `ci.yml`.

### ML Test Selection Not Working

**Problem**: All tests run instead of subset.

**Solution**: 
1. Check that `USE_LAUNCHABLE` is set to `"true"`
2. Verify `LAUNCHABLE_TOKEN` is set in GitHub Secrets
3. Ensure you're on a PR (not main branch)

### AI Analysis Not Running

**Problem**: No AI summary in PR comments.

**Solution**:
1. Check that `USE_MODELS_SUMMARY` is set to `"true"`
2. Verify GitHub Models is enabled in repo settings
3. Ensure tests actually failed

### Timeout Tests Failing

**Problem**: Timeout tests consistently fail.

**Solution**: Increase timeout in `pytest.ini`:
```ini
timeout = 60  # Increase from 30 to 60 seconds
```

## 📚 Additional Resources

- [test_scenarios.md](test_scenarios.md) - Detailed scenario descriptions
- [pytest.ini](pytest.ini) - Pytest configuration
- [.github/workflows/ci.yml](.github/workflows/ci.yml) - CI/CD pipeline

## 🎉 Success Indicators

You'll know self-healing is working when you see:

✅ Tests retry automatically after failures  
✅ ML selects only relevant tests  
✅ AI provides actionable failure summaries  
✅ Pipeline recovers from transient failures  
✅ CI/CD completes faster with intelligent test selection  
✅ Fewer false-positive failures  

## 🚀 Next Steps

1. Run tests locally to verify they work
2. Push changes to GitHub
3. Create a PR to trigger CI/CD
4. Watch the self-healing mechanisms in action
5. Review AI summaries for insights
6. Iterate and improve test reliability

---

**Happy Testing! 🎉**

