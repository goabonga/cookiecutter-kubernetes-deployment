
# 🚀 cookiecutter-kustomize-deployment

**cookiecutter-kustomize-deployment** is a template generator for deploying applications using Helm and Kustomize on Kubernetes. This template facilitates the creation of environment-specific configurations for any Helm applications, supporting both development and production configurations via Kustomize overlays.

## 🎯 Features

- **Helm & Kustomize Deployment**: Automates the generation of Helm charts and Kustomize overlays, making deployments modular and environment-specific.
- **Dynamic Helm Chart Details**: Uses a post-generation script to automatically retrieve the latest chart versions and values, keeping deployments up-to-date.
- **Environment Overlays**: Separate `development` and `production` overlays to streamline configuration management for different Kubernetes environments.
- **Automated Setup via Post-Generation Hook**: Automatically configures Helm and Kustomize files to reduce manual setup, ensuring that the deployment is production-ready out of the box.

## 📂 Project Structure

The generated project includes:

```plaintext
keycloak/
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
│   │   └── keycloak-24.1.0.tgz      # Packaged Helm chart
│   ├── Chart.yaml                   # Helm chart metadata
│   ├── README.md                    # Documentation for Helm chart
│   └── values.yaml                  # Default Helm values
└── upstream.sh                      # Script to handle Helm and Kustomize setup
```

## 📦 Getting Started

1. **Install CookieCutter**:

   Ensure that you have CookieCutter installed:

   ```bash
   pip install cookiecutter
   ```

2. **Install Helm and Helm-Docs**:

   Helm and Helm-Docs are required to use this CookieCutter template:

   ```bash
   # Install Helm
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

   # Install Helm-Docs
   curl -sSL "https://github.com/norwoodj/helm-docs/releases/download/v1.14.2/helm-docs_1.14.2_Linux_x86_64.tar.gz" | tar xz
   sudo mv helm-docs /usr/local/bin/

   ```

3. **Generate a New Project**:

   Use CookieCutter with this template to initialize a new deployment:

   ```bash
   cookiecutter https://github.com/goabonga/cookiecutter-kustomize-deployment.git
   ```

   This will prompt you for basic project details (e.g., project name, namespace, Helm repository). Once completed, the project structure will be generated.

4. **Configure Your Deployment**:

   Inside the generated project directory:
   - **Customize Values**: Modify `values.yaml` under the `upstream` directory to adjust Helm chart settings.
   - **Environment-specific Configurations**: Edit `secret-generator.yaml` and other overlay configurations in `overlays/production` or `overlays/development` as needed.

5. **Deploy Your Application**:

   Use Kustomize and Helm commands to deploy the application, adjusting the environment as needed:

   ```bash
   # For development
   kubectl apply -k overlays/development

   # For production
   kubectl apply -k overlays/production
   ```

## 🔧 Post-Generation Script

The template includes a `post_gen_project.py` hook script that automatically sets up the Helm chart and configures values for Helm deployment. Here’s how it works:

- **Fetch Helm Chart Details**: Retrieves the latest version of the Helm chart and populates `Chart.yaml` and `values.yaml` accordingly.
- **Chart Customization**: Generates a `Chart.yaml` with the specified app version and alias (if provided).
- **Run Initialization Scripts**: Executes `upstream.sh` to handle any additional setup and initializes `helm-docs` for automatic documentation generation.

## 🤑 Customization Options

The configuration file allows setting the following parameters for project customization:

```json
{
  "name": "keycloak",
  "version": "latest",
  "namespace": "default",
  "alias": null,
  "repository": "https://charts.bitnami.com/bitnami"
}
```

## 🤓 Contributing

We welcome contributions to enhance this template. If you have suggestions, feel free to submit a pull request or open an issue.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Happy deploying with **cookiecutter-kustomize-deployment**! 🚀