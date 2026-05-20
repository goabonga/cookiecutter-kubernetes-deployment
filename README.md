# cookiecutter-kubernetes-deployment

[![CI](https://github.com/goabonga/cookiecutter-kubernetes-deployment/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/goabonga/cookiecutter-kubernetes-deployment/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/goabonga/cookiecutter-kubernetes-deployment/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template that scaffolds
a Kubernetes deployment combining a **Helm** upstream chart with **Kustomize**
base + per-environment overlays. A post-generation hook resolves the chart
version and renders its `values.yaml` automatically.

## Features

- **Helm + Kustomize** — a vendored upstream Helm chart wrapped in a Kustomize
  `base` with `development` / `production` overlays.
- **Dynamic chart details** — the post-gen hook pulls the latest chart version
  and values so the deployment starts up to date.
- **Generated governance** — the rendered project ships its own README,
  CONTRIBUTING, CODE_OF_CONDUCT and a license of your choice (MIT / GPL /
  Proprietary).

## Requirements

- Python 3.12+
- [Helm](https://helm.sh/docs/intro/install/) and
  [helm-docs](https://github.com/norwoodj/helm-docs) on your `PATH` — the
  post-generation hook calls them (with network access to the chart repo).

## Usage

Generate a deployment straight from GitHub:

```bash
uvx cookiecutter gh:goabonga/cookiecutter-kubernetes-deployment
# or: cookiecutter gh:goabonga/cookiecutter-kubernetes-deployment
```

Or install the published template from PyPI and bake the bundled copy:

```bash
pip install cookiecutter-kubernetes-deployment
cookiecutter "$(python -c 'import cookiecutter_kubernetes_deployment as p; print(p.__path__[0])')"
```

You'll be prompted for the chart `name`, `namespace`, `repository`, `alias`,
`author_name` and `license`. The generated tree:

```
<name>/
├── base/kustomization.yaml
├── overlays/
│   ├── development/{kustomization,secret-generator}.yaml
│   └── production/{kustomization,secret-generator}.yaml
├── resources/kustomization.yaml
├── upstream/                 # Helm chart (Chart.yaml, values.yaml, …)
├── upstream.sh
└── README.md / CONTRIBUTING.md / CODE_OF_CONDUCT.md / LICENSE
```

Deploy with Kustomize:

```bash
kubectl apply -k overlays/development
kubectl apply -k overlays/production
```

## Development

```bash
git clone https://github.com/goabonga/cookiecutter-kubernetes-deployment.git
cd cookiecutter-kubernetes-deployment
uv sync
uv run pytest          # bakes the template (needs Helm + helm-docs + network)
uvx cookiecutter .     # generate a project from the working copy
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow, the commit-message
convention and the release process. By participating you agree to the
[Code of Conduct](CODE_OF_CONDUCT.md). Security issues: see
[SECURITY.md](SECURITY.md).

## License

Distributed under the [MIT License](LICENSE).
