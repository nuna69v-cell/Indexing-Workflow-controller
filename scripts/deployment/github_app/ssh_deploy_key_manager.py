import os
import subprocess
from typing import Tuple, Optional, Dict
import requests
from github_api_manager import GitHubAppManager

class SSHKeyManager:
    """
    Manages generation and deployment of SSH Deploy Keys.
    """
    def __init__(self, github_manager: GitHubAppManager):
        self.github_manager = github_manager

    def generate_key(self, key_name: str, key_dir: str = "/tmp") -> Tuple[str, str]:
        """
        Generate an Ed25519 SSH key pair.
        Returns: Tuple of (private_key_content, public_key_content)
        """
        key_path = os.path.join(key_dir, key_name)

        # Remove old keys if they exist
        if os.path.exists(key_path):
            os.remove(key_path)
        if os.path.exists(f"{key_path}.pub"):
            os.remove(f"{key_path}.pub")

        # Generate new key
        # Using ed25519 for modern security
        cmd = [
            "ssh-keygen",
            "-t", "ed25519",
            "-N", "", # Empty passphrase
            "-f", key_path,
            "-q" # Quiet mode
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to generate SSH key: {e.stderr.decode()}")

        with open(key_path, 'r') as f:
            private_key = f.read()

        with open(f"{key_path}.pub", 'r') as f:
            public_key = f.read()

        return private_key, public_key

    def add_deploy_key(self, owner: str, repo: str, title: str, public_key: str, read_only: bool = True, installation_id: Optional[str] = None) -> Dict:
        """
        Add an SSH deploy key to a GitHub repository.
        """
        headers = self.github_manager.get_auth_headers(installation_id)
        url = f"{self.github_manager.api_base}/repos/{owner}/{repo}/keys"

        payload = {
            "title": title,
            "key": public_key,
            "read_only": read_only
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def save_private_key(self, private_key: str, path: str):
         """Securely save a private key to disk."""
         # Ensure directory exists
         os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

         # Write key
         with open(path, 'w') as f:
             f.write(private_key)

         # Set secure permissions (0600)
         os.chmod(path, 0o600)
