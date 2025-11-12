#!/usr/bin/env python3
"""GitHubOrgClient module"""

from typing import List, Dict
from utils import get_json, memoize


class GithubOrgClient:
    """A client to interact with the GitHub API for organization data."""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str):
        """Initialize the client with the org name."""
        self.org_name = org_name
    
    @property
    @memoize
    def org(self) -> Dict:
        """Fetch and return the organization information."""
        url = self.ORG_URL.format(org=self.org_name)
        return get_json(url)

    @property
    def _public_repos_url(self) -> str:
        """Return the URL to the list of public repositories."""
        return self.org.get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        """Return the list of public repositories."""
        repos = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos]

        if license is None:
            return repo_names

        # Filter repos by license
        return [
            repo["name"]
            for repo in repos
            if self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repo has the given license key."""
        try:
            return repo["license"]["key"] == license_key
        except (KeyError, TypeError):
            return False