
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

Pull requests trigger the validation job so every PR runs the full linting, type-checking, security, and test suite before it is eligible to merge. When a push targets the `main` branch and the validation job succeeds, the workflow automatically builds the Docker image and publishes it to Docker Hub. Because the publish stage only runs for pushes to `main`, you will see it marked as **skipped** on pull request builds—this is expected so unmerged code does not push images prematurely.

See `.github/workflows/ci.yml` for details.

### Suggested Next Stage

To extend the pipeline beyond validation, add a deployment stage that builds the Docker image and publishes it to your chosen container registry. After pushing the image, trigger an environment-specific deploy (for example, using GitHub Environments with manual approvals or Infrastructure as Code such as Terraform) so new commits automatically roll out once they pass the quality gate established by the existing jobs.

### Deploying the published image

Once the image (for example `spakai/cicd-gitea`) is available on Docker Hub, you can promote it to each environment with a lightweight run job. A minimal manual workflow looks like:

```bash
# Pull the image that GitHub Actions published
docker pull spakai/cicd-gitea:latest

# Run it locally for a smoke test
docker run --rm -p 8000:8000 \
  -e FIB_SERVER_HOST=0.0.0.0 \
  -e FIB_SERVER_PORT=8000 \
  spakai/cicd-gitea:latest

# Open http://localhost:8000/fib/?n=10 and verify the API responds.
```

For repeatable deployments, codify the runtime configuration. Two common options are:

- **Docker Compose:** define dependencies (for example, a reverse proxy) and share the stack via version-controlled YAML.
- **Kubernetes/Helm:** create manifests that reference the image tag produced by CI and leverage progressive delivery strategies such as blue/green or canary releases.

After you are comfortable with the manual steps, create a `deploy` job in GitHub Actions that runs only after the publish job succeeds. The job can target self-hosted runners (for on-premises servers, like Gitea or a private VM) or call out to your infrastructure provider via Terraform, Ansible, or a platform-specific deployment action. Make sure to:

1. Promote immutable tags (for example, `${{ github.sha }}`) so each deployment is traceable back to a commit.
2. Use environments and required reviewers in GitHub Actions to gate production deploys.
3. Capture deployment status with `deployment` events so GitHub’s Environment dashboard and audit trail stay in sync with your releases.

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
