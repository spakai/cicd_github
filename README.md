
# cicd_gitea

An example Python project demonstrating CI/CD with GitHub Actions.

## Features
- Minimal HTTP API for Fibonacci numbers
- Unit tests and coverage reporting
- Linting and static analysis (flake8, mypy, bandit, pylint)
- Automated CI pipeline with GitHub Actions

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
Clone the repo and install dependencies:

```bash
git clone https://github.com/spakai/cicd_gitea.git
cd cicd_gitea
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running Tests & Linting

```bash
pytest --cov=fib --cov-report=term-missing
flake8
mypy fib tests
bandit -r fib
pylint fib
```

## Usage

Run the HTTP server:

```bash
python -m fib.api
```
Then access: `http://127.0.0.1:8000/fib/?n=10`

## CI/CD Pipeline

On every push or pull request, GitHub Actions will:
- Install dependencies
- Run linting and static analysis
- Run tests and report coverage

See `.github/workflows/ci.yml` for details.

## Contributing
Pull requests are welcome! Please ensure code passes all checks before submitting.

## License
MIT
