import os
import time
from typing import Dict, List, Optional

import jwt
import requests


class GitHubAppManager:
    """
    Manages GitHub API interactions, either as a GitHub App or with a PAT.
    """

    def __init__(
        self,
        app_id: Optional[str] = None,
        private_key_path: Optional[str] = None,
        pat_token: Optional[str] = None,
    ):
        self.app_id = app_id or os.getenv("GITHUB_APP_ID")
        self.private_key_path = private_key_path or os.getenv(
            "GITHUB_APP_PRIVATE_KEY_PATH"
        )
        self.pat_token = pat_token or os.getenv("GITHUB_TOKEN")

        self.api_base = "https://api.github.com"

        if not self.pat_token and not (self.app_id and self.private_key_path):
            raise ValueError(
                "Must provide either a PAT token or both App ID and Private Key Path."
            )

        self._jwt_token = None
        self._jwt_expires_at = 0

    def _get_jwt(self) -> str:
        """Generate a JWT for authenticating as a GitHub App."""
        now = int(time.time())
        if self._jwt_token and now < self._jwt_expires_at:
            return self._jwt_token

        with open(self.private_key_path, "r") as key_file:
            private_key = key_file.read()

        payload = {
            "iat": now,
            "exp": now + (10 * 60),  # JWT expires in 10 minutes maximum
            "iss": self.app_id,
        }

        self._jwt_token = jwt.encode(payload, private_key, algorithm="RS256")
        self._jwt_expires_at = now + (9 * 60)  # Refresh slightly before expiration
        return self._jwt_token

    def _get_installation_token(self, installation_id: str) -> str:
        """Get an installation access token for a specific app installation."""
        jwt_token = self._get_jwt()
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.post(
            f"{self.api_base}/app/installations/{installation_id}/access_tokens",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["token"]

    def get_auth_headers(self, installation_id: Optional[str] = None) -> Dict[str, str]:
        """Get the appropriate authorization headers based on authentication method."""
        if self.pat_token:
            return {
                "Authorization": f"token {self.pat_token}",
                "Accept": "application/vnd.github.v3+json",
            }

        if installation_id:
            token = self._get_installation_token(installation_id)
            return {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            }

        # Fallback to authenticating as the app itself
        return {
            "Authorization": f"Bearer {self._get_jwt()}",
            "Accept": "application/vnd.github.v3+json",
        }

    def list_installations(self) -> List[Dict]:
        """List all installations of this GitHub App."""
        if self.pat_token:
            raise ValueError("Cannot list installations when authenticated with a PAT.")

        headers = self.get_auth_headers()
        response = requests.get(f"{self.api_base}/app/installations", headers=headers)
        response.raise_for_status()
        return response.json()

    def list_repositories(self, installation_id: Optional[str] = None) -> List[Dict]:
        """List repositories accessible to the token or app installation."""
        headers = self.get_auth_headers(installation_id)

        if self.pat_token:
            url = f"{self.api_base}/user/repos"
        else:
            url = f"{self.api_base}/installation/repositories"

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return (
            data.get("repositories", data)
            if isinstance(data, dict) and "repositories" in data
            else data
        )

    def create_environment(
        self,
        owner: str,
        repo: str,
        environment_name: str,
        installation_id: Optional[str] = None,
    ) -> Dict:
        """Create or update an environment in a repository."""
        headers = self.get_auth_headers(installation_id)
        url = f"{self.api_base}/repos/{owner}/{repo}/environments/{environment_name}"

        # We can add wait_timer, reviewers etc to payload if needed
        response = requests.put(url, headers=headers, json={})
        response.raise_for_status()
        return response.json()

    def get_repo_public_key(
        self, owner: str, repo: str, installation_id: Optional[str] = None
    ) -> Dict:
        """Get the public key for a repository to encrypt secrets."""
        headers = self.get_auth_headers(installation_id)
        url = f"{self.api_base}/repos/{owner}/{repo}/actions/secrets/public-key"

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create_repository_secret(
        self,
        owner: str,
        repo: str,
        secret_name: str,
        encrypted_value: str,
        key_id: str,
        installation_id: Optional[str] = None,
    ) -> bool:
        """Create or update a repository secret."""
        headers = self.get_auth_headers(installation_id)
        url = f"{self.api_base}/repos/{owner}/{repo}/actions/secrets/{secret_name}"

        payload = {"encrypted_value": encrypted_value, "key_id": key_id}

        response = requests.put(url, headers=headers, json=payload)
        return response.status_code in [201, 204]

    def create_environment_secret(
        self,
        owner: str,
        repo: str,
        env_name: str,
        secret_name: str,
        encrypted_value: str,
        key_id: str,
        repository_id: int,
        installation_id: Optional[str] = None,
    ) -> bool:
        """Create or update an environment secret."""
        headers = self.get_auth_headers(installation_id)
        url = f"{self.api_base}/repositories/{repository_id}/environments/{env_name}/secrets/{secret_name}"

        payload = {"encrypted_value": encrypted_value, "key_id": key_id}

        response = requests.put(url, headers=headers, json=payload)
        return response.status_code in [201, 204]
