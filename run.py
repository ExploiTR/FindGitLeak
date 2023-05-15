import os
import shutil
import requests
import argparse
from git import Repo
import gc

def main(mode):
    # Configure your token and the user you're searching as well as the string you're searching for
    token = 'create a personal fine-grained token'
    headers = {'Authorization': f'token {token}'}
    username = 'whoami'  # replace with the username
    search_string = 'storePassword'  # I was searching for password leak in android build.gradle, shortens the search

    # Base URL for the GitHub API
    base_url = 'https://api.github.com'

    # Headers for authorization
    headers = {'Authorization': f'token {token}'}

    # Create a directory to clone the repositories into
    os.makedirs('repos', exist_ok=True)

    # Get the list of repositories for the specified user
    response = requests.get(f'{base_url}/users/{username}/repos', headers=headers)
    repos = response.json()

    # Prepare an empty list to save the repositories where the search string was found
    found_in_repos = []

    # Clone each repository, checkout each commit and search for the string in build.gradle files
    for repo in repos:
        repo_name = repo['name']
    
        # Skip this repository if it's a fork
        if repo['fork']:
            print(f"\nSkipping forked repository {repo_name}...")
            continue

        print(f'\nProcessing repository: {repo_name}')

        # Clone the repository
        repo_dir = f'repos/{repo_name}'
        if not os.path.exists(repo_dir):
            print(f'Cloning repository: {repo_name}')
            Repo.clone_from(repo['clone_url'], repo_dir)

        # Open the repository
        repo_obj = Repo(repo_dir)

        if mode == 'c':
            # Checkout each commit and search for the string in build.gradle files
            for commit in repo_obj.iter_commits():
                process_commit(commit, repo_obj, repo_name, search_string, username, found_in_repos)

        elif mode == 'b':
            # Checkout each branch and search for the string in build.gradle files
            for branch in repo_obj.branches:
                print(f'Checking out branch: {branch}')
                branch.checkout()
                process_commit(branch.commit, repo_obj, repo_name, search_string, username, found_in_repos)

        # Release resources
        del repo_obj
        gc.collect()

        # Clean up the repository directory to save disk space
        shutil.rmtree(repo_dir, ignore_errors=True)

    # Print the list of repositories where the search string was found
    if found_in_repos:
        print("\nThe search string was found in the following repositories and commits:")
        for repo_name, commit_link in found_in_repos:
            print(f'Repository: {repo_name}, Commit link: {commit_link}')
    else:
        print("\nThe search string was not found in any repositories.")


def process_commit(commit, repo_obj, repo_name, search_string, username, found_in_repos):
    try:
        print(f'Checking out commit: {commit.hexsha}')
        repo_obj.git.checkout(commit.hexsha)

        # Search for build.gradle files in the repository
        for root, dirs, files in os.walk(repo_obj.working_dir):
            if 'build.gradle' in files:
                with open(os.path.join(root, 'build.gradle')) as f:
                    if search_string in f.read():
                        print(f'Found "{search_string}" in commit {commit.hexsha} of repository {repo_name}')
                        commit_link = f'https://github.com/{username}/{repo_name}/commit/{commit.hexsha}'
                        print(f'Commit link: {commit_link}')
                        found_in_repos.append((repo_name, commit_link))
                        return
    except Exception as e:
        print(f'Error processing commit {commit.hexsha}: {str(e)}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search for a string in all commits or active branches of GitHub repos.')
    parser.add_argument('mode', type=str, choices=['c', 'b'], help='Mode of operation: "c" for all commits, "b" for active branches')

    args = parser.parse_args()

    main(args.mode)
