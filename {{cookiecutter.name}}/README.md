
# {{cookiecutter.name}} deployment

This repository contains the infrastructure configuration for deploying {{cookiecutter.name}} using a combination of Helm and Kustomize. The directory structure is generated with a cookie cutter template and is organized to support multiple environments, including development and production.

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
- [Environments](#environments)
- [Usage](#usage)
- [Updating the Upstream Helm Chart](#updating-the-upstream-helm-chart)
- [Contributing](#contributing)
- [License](#license)

## Overview

This deployment setup uses Helm to manage {{cookiecutter.name}} resources and Kustomize to overlay environment-specific configurations, providing a flexible approach for managing configurations across development and production environments.

## Directory Structure

The main folders and files are organized as follows:

```plaintext
{{cookiecutter.name}}/
├── base
│   └── kustomization.yaml           # Base configurations for Kustomize
├── overlays
│   ├── development
│   │   ├── kustomization.yaml       # Development-specific overlay configurations
│   │   └── secret-generator.yaml    # Secrets for development environment
│   └── production
│       ├── kustomization.yaml       # Production-specific overlay configurations
│       └── secret-generator.yaml    # Secrets for production environment
├── README.md                        # Project documentation
├── resources
│   ├── kustomization.yaml           # Additional Kustomize resources
│   └── upstream.yaml                # Configurations for the Helm chart
├── upstream
│   ├── Chart.lock                   # Lock file for Helm dependencies
│   ├── charts
│   │   └── {{cookiecutter.name}}-24.1.0.tgz      # Packaged Helm chart
│   ├── Chart.yaml                   # Helm chart metadata
│   ├── README.md                    # Documentation for Helm chart
│   └── values.yaml                  # Default Helm values
└── upstream.sh                      # Script to handle Helm and Kustomize setup
```

### Key Components

- **base/**: Contains the base Kustomize configuration that can be applied to any environment.
- **overlays/**: Contains environment-specific configurations for development and production, including custom secrets.
- **resources/**: Includes additional resources for Kustomize, like the upstream configuration.
- **upstream/**: Houses the Helm chart and dependencies for {{cookiecutter.name}}.
- **upstream.sh**: Script for managing Helm and Kustomize setup and updates.

## Getting Started

### Prerequisites

- [Helm](https://helm.sh/) 3.x
- [Kustomize](https://kustomize.io/)
- [ksops](https://github.com/viaduct-ai/kustomize-sops): Required for handling encrypted secrets with SOPS and Kustomize
- [helm-docs](https://github.com/norwoodj/helm-docs): For generating Helm documentation
- Kubernetes cluster with access to deploy resources

### Installation

1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd {{cookiecutter.name}}
   ```

2. Configure secrets in the `overlays/development/secret-generator.yaml` and `overlays/production/secret-generator.yaml` files.

3. Deploy to your desired environment (see [Usage](#usage)).

## Environments

This setup supports two main environments:
- **Development**: Configurations in `overlays/development`
- **Production**: Configurations in `overlays/production`

Each environment has its own secrets and customizations, managed by Kustomize overlays.

## Usage

### Deploying {{cookiecutter.name}}

To deploy {{cookiecutter.name}} to a specific environment, use the following commands:

#### Development
If you are using ksops to manage secrets, use the command with `--enable-alpha-plugins` and `--enable-exec`:

```bash
kustomize build --enable-alpha-plugins --enable-exec overlays/development | kubectl apply -f -
```

#### Production
```bash
kubectl apply -k overlays/production
```

### Cleaning Up

To remove the deployment from a specific environment:
```bash
kubectl delete -k overlays/<environment>
```

## Updating the Upstream Helm Chart

To update the {{cookiecutter.name}} Helm chart:

1. Modify the `values.yaml` in `upstream` with any new configurations required.
2. Regenerate the `resources/upstream.yaml` and the documentation by executing the `upstream.sh` script:
   ```bash
   ./upstream.sh
   ```

## Contributing

Please see the `CONTRIBUTING.md` file for guidelines on contributing to this project.

## License

This project is licensed under the [MIT License](LICENSE).