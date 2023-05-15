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

### Disclaimer:
Please use this script responsibly and respect the privacy and security of others. Ensure that you have the necessary permissions to search the repositories. The script is provided as-is without any warranty or guarantee of its effectiveness. Use it at your own risk.
