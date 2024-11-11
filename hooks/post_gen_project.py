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
    alias = {% if cookiecutter.alias != None %}'{{cookiecutter.alias}}'{% else%}None{% endif %}
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

    helm_version, helm_app_version, helm_repository_chart = get_helm_info(name)
    
    create_chart_yaml(name, helm_version, helm_app_version, helm_repository, alias)
    create_values_yaml(name, helm_version, helm_repository_chart, alias)
    subprocess.call(f"./upstream.sh")
    subprocess.call(f"helm-docs")


if __name__ == "__main__":
    main()
