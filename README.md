
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

The module honours two optional environment variables when launched directly:

| Variable | Purpose | Default |
| --- | --- | --- |
| `FIB_SERVER_HOST` | Network interface bound by the development server. Use `0.0.0.0` inside containers. | `127.0.0.1` |
| `FIB_SERVER_PORT` | TCP port exposed by the server. | `8000` |

## CI/CD Pipeline

On every push or pull request, GitHub Actions will:
- Install dependencies
- Run linting and static analysis
- Run tests and report coverage

When a push targets the `main` branch and the validation job succeeds, the workflow automatically builds the Docker image and publishes it to Docker Hub.

See `.github/workflows/ci.yml` for details.

### Suggested Next Stage

To extend the pipeline beyond validation, add a deployment stage that builds the Docker image and publishes it to your chosen container registry. After pushing the image, trigger an environment-specific deploy (for example, using GitHub Environments with manual approvals or Infrastructure as Code such as Terraform) so new commits automatically roll out once they pass the quality gate established by the existing jobs.

### Publishing to Docker Hub from GitHub Actions

The repository now includes a `publish` job that builds the Docker image and pushes it to Docker Hub whenever a commit is pushed to the `main` branch and all validation checks pass. To make the job succeed you must supply Docker Hub credentials via GitHub secrets:

1. **Create a Docker Hub access token:** Log into [hub.docker.com](https://hub.docker.com/), open **Account Settings → Security → Access Tokens**, and generate a new token. Tokens can be revoked and are safer than using your password directly.
2. **Store the credentials as GitHub secrets:** In **Settings → Secrets and variables → Actions**, add two repository secrets:
   - `DOCKERHUB_USERNAME`: your Docker Hub username (for example `spakai`).
   - `DOCKERHUB_TOKEN`: the access token created above.

With the secrets configured, the workflow will:

```yaml
publish:
  needs:
    - test
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  steps:
    - uses: actions/checkout@v4
    - uses: docker/setup-buildx-action@v2
    - uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    - uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKERHUB_USERNAME }}/cicd-gitea:latest
          ${{ secrets.DOCKERHUB_USERNAME }}/cicd-gitea:${{ github.sha }}
```

Adjust the branch filter, tags, or build arguments if you prefer a different release strategy (for example only pushing on version tags or pushing multiple architectures).

## Contributing
Pull requests are welcome! Please ensure code passes all checks before submitting.

## License
MIT
