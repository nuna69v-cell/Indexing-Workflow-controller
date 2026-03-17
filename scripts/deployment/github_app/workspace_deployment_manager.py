import argparse
import os
from typing import Optional

from github_api_manager import GitHubAppManager
from ssh_deploy_key_manager import SSHKeyManager


def deploy_workspace(
    owner: str,
    repo: str,
    workspace_dir: str,
    env_name: str = "production",
    key_name: str = "deploy_key",
    installation_id: Optional[str] = None,
):
    """
    Sets up a deployment workspace with an SSH deploy key and configures the GitHub repository.
    """
    print(
        f"Starting workspace deployment for {owner}/{repo} to {workspace_dir} in environment '{env_name}'..."
    )

    github_manager = GitHubAppManager()
    ssh_manager = SSHKeyManager(github_manager)

    # Ensure workspace directory exists
    os.makedirs(workspace_dir, exist_ok=True)

    # 1. Generate SSH Key Pair
    print(f"Generating SSH key '{key_name}'...")
    private_key, public_key = ssh_manager.generate_key(key_name, workspace_dir)

    # 2. Save private key securely in the workspace
    private_key_path = os.path.join(workspace_dir, key_name)
    ssh_manager.save_private_key(private_key, private_key_path)
    print(f"Private key saved securely to {private_key_path}")

    # 3. Add deploy key to GitHub
    print("Adding public key as a deploy key to the GitHub repository...")
    key_title = f"{env_name}-deploy-key"
    try:
        ssh_manager.add_deploy_key(
            owner=owner,
            repo=repo,
            title=key_title,
            public_key=public_key,
            read_only=False,  # Needed if deployment jobs push code/tags
            installation_id=installation_id,
        )
        print(f"Successfully added deploy key '{key_title}'.")
    except Exception as e:
        print(f"Warning: Failed to add deploy key (it might already exist). Error: {e}")

    # 4. Configure GitHub Environment
    print(f"Creating/updating GitHub environment '{env_name}'...")
    try:
        github_manager.create_environment(owner, repo, env_name, installation_id)

        # We need the repository ID for environment secrets
        repos = github_manager.list_repositories(installation_id)
        repo_id = None
        for r in repos:
            if r["name"] == repo and r["owner"]["login"] == owner:
                repo_id = r["id"]
                break

        if not repo_id:
            # Fallback to fetching specific repo if not in the list (pagination etc)
            headers = github_manager.get_auth_headers(installation_id)
            import requests

            r = requests.get(
                f"{github_manager.api_base}/repos/{owner}/{repo}", headers=headers
            )
            r.raise_for_status()
            repo_id = r.json()["id"]

        # 5. Add Private Key as an Environment Secret
        print("Fetching repository public key for secret encryption...")
        pub_key_info = github_manager.get_repo_public_key(owner, repo, installation_id)

        print("Encrypting and uploading private key to environment secrets...")
        # Note: We need to base64 encode then encrypt the secret.
        # This requires the pynacl or cryptography library. We'll use the one available in the system
        # Assuming cryptography is available based on other files in the project
        try:
            import base64

            from nacl import encoding, public

            public_key = public.PublicKey(
                pub_key_info["key"].encode("utf-8"), encoding.Base64Encoder()
            )
            sealed_box = public.SealedBox(public_key)
            encrypted = sealed_box.encrypt(private_key.encode("utf-8"))
            encrypted_value = base64.b64encode(encrypted).decode("utf-8")

            github_manager.create_environment_secret(
                owner=owner,
                repo=repo,
                env_name=env_name,
                secret_name="SSH_DEPLOY_KEY",
                encrypted_value=encrypted_value,
                key_id=pub_key_info["key_id"],
                repository_id=repo_id,
                installation_id=installation_id,
            )
            print("Successfully added SSH_DEPLOY_KEY to environment secrets.")
        except ImportError:
            print(
                "Warning: 'cryptography' library not found. Skipping secret creation. You'll need to manually add the secret."
            )
            print(f"The private key is located at: {private_key_path}")

    except Exception as e:
        print(f"Warning: Failed to configure environment. Error: {e}")

    print("\nWorkspace deployment setup complete!")
    print(f"Private Key Path: {private_key_path}")
    print(f"Environment: {env_name}")
    print(f"Secret Name: SSH_DEPLOY_KEY (contains the private key)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Set up a deployment workspace for a GitHub repository"
    )
    parser.add_argument("--owner", required=True, help="GitHub repository owner")
    parser.add_argument("--repo", required=True, help="GitHub repository name")
    parser.add_argument("--dir", required=True, help="Workspace directory path")
    parser.add_argument(
        "--env", default="production", help="Environment name (default: production)"
    )
    parser.add_argument("--installation-id", help="Optional GitHub App Installation ID")

    args = parser.parse_args()

    deploy_workspace(
        owner=args.owner,
        repo=args.repo,
        workspace_dir=args.dir,
        env_name=args.env,
        installation_id=args.installation_id,
    )
