
# Contributing to {{cookiecutter.name}}

Thank you for considering contributing to {{cookiecutter.name}}! Contributions are welcome and encouraged. This guide provides an overview of the guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can You Contribute?](#how-can-you-contribute)
- [Getting Started](#getting-started)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Issues and Bugs](#issues-and-bugs)

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing. All contributors are expected to adhere to it to foster an inclusive and safe environment for everyone.

## How Can You Contribute?

There are several ways to contribute to {{cookiecutter.name}}:

1. **Reporting Bugs**: Found a bug? Open an issue describing the problem.
2. **Suggesting Features**: Have a feature in mind? Open an issue to discuss it.
3. **Writing Code**: Fixing bugs or implementing new features is greatly appreciated.
4. **Improving Documentation**: Good documentation is crucial! Feel free to suggest or make improvements.

## Getting Started

1. **Fork the Repository**: Fork this repository to your GitHub account.
2. **Clone the Repository**: Clone your forked repository to your local machine:
   ```bash
   git clone <repo-url>
   cd {{cookiecutter.name}}
   ```
3. **Create a Branch**: Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Install Dependencies**: Install any dependencies required for development.

## Pull Request Process

1. Ensure that your code is well-formatted and follows the project's [coding standards](#coding-standards).
2. Write tests for any new features or bug fixes.
3. Push your changes to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a pull request (PR) from your branch to `main` in the original repository.
5. Describe your changes in the PR, including any relevant issue numbers.
6. Wait for the maintainers to review your PR. They may suggest improvements or request changes.

## Coding Standards

To maintain consistency and quality across the project, please adhere to the following guidelines:

- **Helm Charts**: Follow Helm best practices for chart structure and `values.yaml` configuration. Avoid hardcoding sensitive data and use variables wherever possible. Document Helm charts using `helm-docs` to generate standardized and readable documentation for values and configurations.

- **Kustomize**: Organize Kustomize overlays logically (e.g., `base`, `development`, `production`). Keep environment-specific configurations in the appropriate overlay folders, and avoid duplicating resources between overlays.

- **YAML Formatting**: Keep YAML files clean and readable, with consistent indentation (2 spaces per level). Use comments to clarify complex configurations.

- **Secrets Management**: For sensitive data, use `ksops` or an equivalent tool to handle encrypted secrets. Ensure secrets are organized by environment and kept out of the repository when unencrypted.

- **Documentation**: Use `helm-docs` to automatically generate documentation for Helm charts, making it easy for other users to understand configurable values and chart details. Additionally, add comments in Kustomize files to clarify non-standard or complex configurations.

- **Testing**: Validate all changes using `helm lint` and `kustomize build` to catch syntax issues early. Additionally, test deployments in a staging environment before merging to production.

- **Commit Standards**: Make each modification a separate commit with a clear, descriptive message. For deployment changes, use a structured message format to specify the purpose of each change. Examples:
  - `chore({{cookiecutter.name}}): configure postgresql connection`
  - `chore({{cookiecutter.name}}): configure smtp connection`
  - `feat({{cookiecutter.name}}): add custom metrics exporter`

  Following this structure keeps commit history clean and makes it easy to track specific configuration changes over time.


## Issues and Bugs

If you find a bug or have an issue, please submit a [new issue](https://github.com/<github_username>/<repo_name>/issues) on GitHub.

When submitting an issue, please include:

1. A description of the issue and expected behavior.
2. Steps to reproduce the issue.
3. Any relevant logs, screenshots, or other details.

Thank you for contributing to {{cookiecutter.name}}!