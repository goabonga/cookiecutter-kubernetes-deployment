import subprocess
import os
import re
from urllib.parse import urlparse

def slugify(value):
    # Converts a string into a slug format suitable for use as a name.
    value = re.sub(r'[^a-zA-Z0-9-]+', '-', value)
    return value.strip('-').lower()

def helm_repo_add_update(repository_url):
    # Parse the repository URL to get the host and create a slug from it
    parsed_url = urlparse(repository_url)
    repo_host = parsed_url.netloc
    repo_name = slugify(repo_host)

    # Adding the helm repository if not already added and then updating
    subprocess.call(f"helm repo add {repo_name} {repository_url}", shell=True)
    subprocess.call("helm repo update", shell=True)

def get_helm_info(name):
    search_result = subprocess.check_output(f"helm search repo {name}", shell=True).decode('utf-8').splitlines()
    helm_version = next((line.split()[1] for line in search_result if name in line), None)
    helm_app_version = next((line.split()[2] for line in search_result if name in line), None)
    helm_repository_chart = next((line.split()[0] for line in search_result if name in line), None)
    return helm_version, helm_app_version, helm_repository_chart

def create_chart_yaml(name, helm_version, helm_app_version, helm_repository, alias=None):
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
    values_result = subprocess.check_output(f"helm show values {helm_repository_chart} --version {helm_version}", shell=True).decode('utf-8')
    values_content = f"{alias or name}:\n" + '\n'.join(f"  {line}" for line in values_result.splitlines())
    
    dir_path = f"./upstream"
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, 'values.yaml'), 'w') as values_file:
        values_file.write(values_content)

def main():
    name = '{{ cookiecutter.name }}'
    alias = {% if cookiecutter.alias != None %}'{{cookiecutter.alias}}'{% else%}None{% endif %}
    helm_repository = '{{ cookiecutter.repository }}'
  
    # Add and update the helm repo
    helm_repo_add_update(helm_repository)

    helm_version, helm_app_version, helm_repository_chart = get_helm_info(name)
    
    create_chart_yaml(name, helm_version, helm_app_version, helm_repository, alias)
    create_values_yaml(name, helm_version, helm_repository_chart, alias)
    subprocess.call(f"./upstream.sh")
    subprocess.call(f"helm-docs")


if __name__ == "__main__":
    main()
