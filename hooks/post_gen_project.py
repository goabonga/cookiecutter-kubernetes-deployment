# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Chris <goabonga@pm.me>

import subprocess
import os
import re
from urllib.parse import urlparse
import shutil

def copy_license():
    """
    Copie le fichier de license choisi dans le fichier LICENSE à la racine du projet.
    """
    license_choice = "{{ cookiecutter.license }}"
    license_filename = f"LICENSE_{license_choice}"

    # Chemins pour le fichier de destination et le fichier source
    destination = "LICENSE"

    source = os.path.join("licenses", f"LICENSE_{license_choice}")

    try:
        shutil.copyfile(source, destination)
        print(f"Licence '{license_choice}' copiée dans le fichier LICENSE")
    except FileNotFoundError:
        print(f"Erreur : Le fichier de license '{license_filename}' est introuvable.")
    shutil.rmtree(os.path.join("licenses"))

def slugify(value):
    # Converts a string into a slug format suitable for use as a name.
    value = re.sub(r'[^a-zA-Z0-9-]+', '-', value)
    return value.strip('-').lower()

def is_oci_repository(repository_url):
    # OCI registries are referenced either with an explicit "oci://" scheme or
    # as a bare registry host/path (e.g. ghcr.io/owner/charts) without a scheme.
    scheme = urlparse(repository_url).scheme
    return scheme in ("", "oci")

def oci_chart_ref(repository_url, name):
    # Build the fully qualified OCI chart reference (oci://host/path/name).
    base = repository_url.rstrip('/')
    if not base.startswith("oci://"):
        base = "oci://" + base
    return f"{base}/{name}"

def helm_repo_add_update(repository_url):
    # OCI registries are pulled directly and must not be registered as a repo.
    if is_oci_repository(repository_url):
        return

    # Parse the repository URL to get the host and create a slug from it
    parsed_url = urlparse(repository_url)
    repo_host = parsed_url.netloc
    repo_name = slugify(repo_host)

    # Adding the helm repository if not already added and then updating
    subprocess.call(f"helm repo add {repo_name} {repository_url}", shell=True)
    subprocess.call("helm repo update", shell=True)

def parse_chart_metadata(chart_yaml):
    # Extract version/appVersion from the YAML emitted by `helm show chart`.
    version = next((line.split(":", 1)[1].strip() for line in chart_yaml.splitlines() if line.startswith("version:")), None)
    app_version = next((line.split(":", 1)[1].strip() for line in chart_yaml.splitlines() if line.startswith("appVersion:")), None)
    return version, app_version

def get_helm_info(name, repository_url, version=None):
    # Resolve the chart reference: OCI pulls use oci://host/path/name, classic
    # HTTP repositories use the local "<repo-slug>/<name>" alias.
    if is_oci_repository(repository_url):
        helm_repository_chart = oci_chart_ref(repository_url, name)
    else:
        repo_name = slugify(urlparse(repository_url).netloc)
        helm_repository_chart = f"{repo_name}/{name}"

    # Only pin a version when the user requested an explicit one.
    version_flag = f" --version {version}" if version and version != "latest" else ""

    try:
        chart_yaml = subprocess.check_output(
            f"helm show chart {helm_repository_chart}{version_flag}", shell=True
        ).decode('utf-8')
        helm_version, helm_app_version = parse_chart_metadata(chart_yaml)
    except subprocess.CalledProcessError:
        helm_version, helm_app_version = None, None

    # Fall back to the requested version (or a placeholder) so generation never
    # crashes when the chart metadata cannot be fetched.
    if not helm_version:
        helm_version = version if version and version != "latest" else "0.0.0"
    if not helm_app_version:
        helm_app_version = helm_version

    return helm_version, helm_app_version, helm_repository_chart

def create_chart_yaml(name, helm_version, helm_app_version, helm_repository, alias=None):
    # OCI dependencies must declare the repository with an oci:// scheme.
    if is_oci_repository(helm_repository):
        helm_repository = helm_repository.rstrip('/')
        if not helm_repository.startswith("oci://"):
            helm_repository = "oci://" + helm_repository
    chart_content = f"""apiVersion: v2
name: {name}
type: application
version: 0.0.0
appVersion: {helm_app_version}
dependencies:
  - name: {name}
    {'alias: ' + alias + chr(10) + '    ' if alias else ''}version: {helm_version}
    repository: {helm_repository}
"""
    dir_path = f"./upstream"
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, 'Chart.yaml'), 'w') as chart_file:
        chart_file.write(chart_content)

def create_values_yaml(name, helm_version, helm_repository_chart, alias=None):
    # Fetching the upstream defaults can fail (private/unauthenticated registry,
    # network issues); fall back to an empty override block so generation still
    # succeeds and the user can fill values in later.
    version_flag = f" --version {helm_version}" if helm_version and helm_version != "0.0.0" else ""
    try:
        values_result = subprocess.check_output(
            f"helm show values {helm_repository_chart}{version_flag}", shell=True
        ).decode('utf-8')
        values_content = f"{alias or name}:\n" + '\n'.join(f"  {line}" for line in values_result.splitlines())
    except subprocess.CalledProcessError:
        values_content = f"{alias or name}: " + "{}\n"

    dir_path = f"./upstream"
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, 'values.yaml'), 'w') as values_file:
        values_file.write(values_content)

def get_git_repo_url():
    # Retrieve the Git repository URL for the current project
    try:
        repo_url = subprocess.check_output("git config --get remote.origin.url", shell=True).decode('utf-8').strip()
        return repo_url
    except subprocess.CalledProcessError:
        return "No repository found"

def update_with_repo_url(readme_path, repo_url):
    # Replace the placeholder <repo-url> with the actual repository URL
    with open(readme_path, 'r') as file:
        readme_content = file.read()
    
    updated_content = readme_content.replace('<repo-url>', repo_url)
    
    with open(readme_path, 'w') as file:
        file.write(updated_content)

def update_with(readme_path, pattern, value):
    # Replace the placeholder <repo-url> with the actual repository URL
    with open(readme_path, 'r') as file:
        readme_content = file.read()
    
    updated_content = readme_content.replace(pattern, value)
    
    with open(readme_path, 'w') as file:
        file.write(updated_content)

def parse_github_info(repo_url):
    # Handle both SSH (git@github.com:username/repo.git) and HTTPS (https://github.com/username/repo.git) formats
    ssh_pattern = r"git@github\.com:(\w+)/([\w-]+)(?:\.git)?"
    https_pattern = r"https?://github\.com/(\w+)/([\w-]+)(?:\.git)?"
    
    # First, try to match the SSH pattern
    ssh_match = re.match(ssh_pattern, repo_url)
    if ssh_match:
        github_username, repo_name = ssh_match.groups()
        return github_username, repo_name

    # If SSH pattern doesn't match, try HTTPS pattern
    https_match = re.match(https_pattern, repo_url)
    if https_match:
        github_username, repo_name = https_match.groups()
        return github_username, repo_name

    # If neither pattern matches, return None
    return None, None

def update_contributing_with_issue_link(contributing_path, github_username, repo_name):
    # Replace the placeholder in CONTRIBUTING.md with the actual GitHub issue link
    with open(contributing_path, 'r') as file:
        content = file.read()
    
    updated_content = content.replace("<github_username>", f"{github_username}")
    updated_content = updated_content.replace("<repo_name>", f"{repo_name}")
    
    with open(contributing_path, 'w') as file:
        file.write(updated_content)

def main():

    # Exécute la copie de la license
    copy_license()

    name = '{{ cookiecutter.name }}'
    version = '{{ cookiecutter.version }}'
    alias = {% if cookiecutter.alias %}'{{ cookiecutter.alias }}'{% else %}None{% endif %}
    # cookiecutter prompts cannot be left empty, so "none" (any case) and blank
    # values are treated as "no alias".
    if alias is None or alias.strip().lower() in ("", "none"):
        alias = None
    helm_repository = '{{ cookiecutter.repository }}'
  
    # Retrieve the Git repository URL and update README.md
    repo_url = get_git_repo_url()
    update_with_repo_url("README.md", repo_url)
    update_with_repo_url("CONTRIBUTING.md", repo_url)
    

    # Parse GitHub username and repository name from the repo URL
    github_username, repo_name = parse_github_info(repo_url)

    # Update the CONTRIBUTING.md with the actual GitHub issue link
    update_contributing_with_issue_link("CONTRIBUTING.md", github_username, repo_name)
 
    # Add and update the helm repo
    helm_repo_add_update(helm_repository)

    helm_version, helm_app_version, helm_repository_chart = get_helm_info(name, helm_repository, version)
    update_with("README.md", '<helm_version>', helm_version)
    
    create_chart_yaml(name, helm_version, helm_app_version, helm_repository, alias)
    create_values_yaml(name, helm_version, helm_repository_chart, alias)
    subprocess.call(f"./upstream.sh")
    subprocess.call(f"helm-docs")


if __name__ == "__main__":
    main()
