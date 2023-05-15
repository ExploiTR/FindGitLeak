## FindGitLeak

### Description:
This script is designed to search for password leakages in GitHub repositories. It helps identify potential security vulnerabilities by scanning repositories for sensitive information. By leveraging the GitHub API, the script retrieves repositories owned by a specified user and performs a search for passwords within the codebase.

### Usage:
Set up your environment and dependencies.
Configure your GitHub username and access token.
Specify the search string (password) to look for.
Run.

> ###### Note: This script should be used responsibly and only on repositories where you have permission to search. Also, be careful when setting up the access tokens.

#### To delete ?
```
git clone https://github.com/ExploiTR/FindGitLeak.git
cd FindGitLeak
git checkout --orphan latest_branch
git add -A
git commit -am "Remove commit history"
git branch -D master
git branch -m master
git push -f origin master
```
