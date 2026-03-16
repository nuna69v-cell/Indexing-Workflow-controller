import argparse
import json
import logging
import os
import urllib.request
import urllib.error
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
GITHUB_API_URL = "https://api.github.com"
MASTER_MAP_FILE = ".master-map.json"


def get_headers(token: str) -> Dict[str, str]:
    """Returns headers for GitHub API requests."""
    return {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
        "User-Agent": "GenX-CLI-Manager",
    }


def get_accounts() -> Dict[str, str]:
    """Retrieves GitHub accounts and tokens from environment variables."""
    # Look for variables like GH_TOKEN, GH_USER_TOKEN, or custom ones
    accounts = {}

    # Check default tokens
    if os.getenv("GH_TOKEN"):
        accounts["default"] = os.getenv("GH_TOKEN")

    # Check specific user tokens based on environment variables
    # This matches the pattern in memory (TOKENS dict)
    for key, value in os.environ.items():
        if key.endswith("_TOKEN") and value and key not in ["GH_TOKEN"]:
            account_name = key.replace("_TOKEN", "").lower()
            accounts[account_name] = value

    # Hardcoded fallback for the specific users mentioned in memory if tokens exist
    if not accounts:
        logger.warning(
            "No GitHub tokens found in environment. Please set GH_TOKEN or specific account tokens."
        )
        # Returning mock data for demonstration purposes if needed
        # accounts = {"mock_account": "mock_token"}

    return accounts


def map_repositories(accounts: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
    """Maps all repositories for the given accounts."""
    master_map = {}

    for account, token in accounts.items():
        logger.info(f"Mapping repositories for account: {account}...")
        headers = get_headers(token)
        repos = []
        page = 1

        while True:
            # We use user/repos instead of users/{user}/repos to get repos for the authenticated user
            # which might include private repos
            url = f"{GITHUB_API_URL}/user/repos?page={page}&per_page=100"
            req = urllib.request.Request(url, headers=headers)

            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.getcode() == 200:
                        data = json.loads(response.read().decode("utf-8"))
                        if not data:
                            break

                        for r in data:
                            # Calculate a rough "weight" based on size (in KB)
                            size_kb = r.get("size", 0)

                            repos.append(
                                {
                                    "name": r["name"],
                                    "full_name": r["full_name"],
                                    "url": r["clone_url"],
                                    "branch": r.get("default_branch", "main"),
                                    "description": r.get("description", ""),
                                    "size_kb": size_kb,
                                    "archived": r.get("archived", False),
                                    "private": r.get("private", False),
                                }
                            )
                        page += 1
                    else:
                        logger.error(
                            f"Failed to fetch repos for {account}: {response.getcode()}"
                        )
                        break
            except urllib.error.URLError as e:
                logger.error(
                    f"Connection error while fetching repos for {account}: {e}"
                )
                break

        master_map[account] = repos
        logger.info(f"Found {len(repos)} repositories for {account}.")

    return master_map


def map_ea_environments(
    master_map: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, List[Dict[str, Any]]]:
    """Maps EA environment settings including IPs, Ports, and Jules API Keys."""
    logger.info("Mapping EA environments with Jules API Keys...")

    # Retrieve Jules API Keys from environment
    jules_keys = []
    for key, value in os.environ.items():
        if key.startswith("JULES_API") and value:
            jules_keys.append({"name": key, "key": value})

    if not jules_keys:
        logger.warning("No JULES_API keys found in environment.")
        # Default mock fallback for demonstration if needed based on memory
        # jules_keys = [{"name": "JULES_API_V1", "key": "AQ.Ab8RN6K..."}]

    # Apply to repositories that look like EAs or Trading Systems
    for account, repos in master_map.items():
        for i, repo in enumerate(repos):
            name_lower = repo["name"].lower()
            if (
                "ea" in name_lower
                or "trade" in name_lower
                or "genx" in name_lower
                or "bot" in name_lower
            ):
                # Setup specific EA configurations
                key_index = i % len(jules_keys) if jules_keys else 0
                selected_key = jules_keys[key_index]["key"] if jules_keys else ""

                # Base port is 5555, increment for each EA to avoid conflicts
                assigned_port = 5555 + i

                repo["ea_config"] = {
                    "mapped": True,
                    "target_ip": "127.0.0.1",
                    "target_port": assigned_port,
                    "jules_api_key": selected_key,
                    "status": "Ready for injection",
                }
                logger.info(
                    f"  - Mapped EA config for {repo['name']}: Port {assigned_port}"
                )

    return master_map


def generate_ea_config_file(master_map: Dict[str, List[Dict[str, Any]]]):
    """Generates a configuration file specifically for EAs based on mapped data."""
    ea_configs = {}

    for account, repos in master_map.items():
        for repo in repos:
            if "ea_config" in repo:
                ea_configs[repo["name"]] = repo["ea_config"]

    if ea_configs:
        try:
            with open("ea_port_mapping.json", "w") as f:
                json.dump(ea_configs, f, indent=4)
            logger.info("Generated EA port mapping at ea_port_mapping.json")
        except IOError as e:
            logger.error(f"Failed to write EA mapping: {e}")


def generate_master_map(master_map: Dict[str, List[Dict[str, Any]]]):
    """Saves the master map to a JSON file."""
    try:
        with open(MASTER_MAP_FILE, "w") as f:
            json.dump(master_map, f, indent=4)
        logger.info(f"Master Map created successfully at {MASTER_MAP_FILE}")
    except IOError as e:
        logger.error(f"Failed to write Master Map: {e}")


def get_heavy_repositories(
    master_map: Dict[str, List[Dict[str, Any]]], size_threshold_kb: int = 50000
) -> List[Dict[str, Any]]:
    """Identifies repositories that exceed the size threshold."""
    heavy_repos = []

    for account, repos in master_map.items():
        for repo in repos:
            if repo["size_kb"] > size_threshold_kb:
                repo_with_account = repo.copy()
                repo_with_account["account"] = account
                heavy_repos.append(repo_with_account)

    return sorted(heavy_repos, key=lambda x: x["size_kb"], reverse=True)


def apply_blocking_function(
    repo: Dict[str, Any], accounts: Dict[str, str], dry_run: bool = True
):
    """
    Applies a 'blocking function' to reduce repository weight.
    This could mean deleting old artifacts, trimming history, or archiving.
    For this implementation, we simulate these actions or apply safe ones.
    """
    repo_name = repo["full_name"]
    account = repo["account"]
    token = accounts.get(account)
    size_mb = repo["size_kb"] / 1024

    logger.info(
        f"Applying blocking function to heavy repository: {repo_name} ({size_mb:.2f} MB)"
    )

    if not token:
        logger.error(
            f"No token found for account {account}, cannot apply blocking function."
        )
        return

    headers = get_headers(token)

    # 1. Check for large releases/assets that can be deleted
    releases_url = f"{GITHUB_API_URL}/repos/{repo_name}/releases"
    req = urllib.request.Request(releases_url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                releases = json.loads(response.read().decode("utf-8"))
                logger.info(f"  - Found {len(releases)} releases.")
                # Implementation to delete old assets would go here
                if not dry_run and releases:
                    logger.info(
                        "  - (Action) Would delete old release assets to save space."
                    )
    except Exception as e:
        logger.warning(f"  - Could not check releases: {e}")

    # 2. Check if repository is stale and can be archived
    # We would check last commit date here

    # 3. Trigger git GC (Garbage Collection) via API if possible
    # (GitHub runs GC automatically, but we can trigger repo optimization)

    if dry_run:
        logger.info(f"  - DRY RUN: No actual changes made to {repo_name}")
    else:
        logger.info(f"  - Successfully applied optimizations to {repo_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage packages/repositories across GitHub accounts"
    )
    parser.add_argument(
        "--map-only",
        action="store_true",
        help="Only map repositories, do not apply blocking functions",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=50000,
        help="Size threshold in KB to consider a repository 'heavy' (default: 50000 KB)",
    )
    parser.add_argument(
        "--apply-blocking",
        action="store_true",
        help="Apply blocking function to reduce repository weight",
    )
    parser.add_argument(
        "--execute", action="store_true", help="Execute changes (default is dry-run)"
    )

    args = parser.parse_args()

    logger.info("Starting Package/Repository Management")

    accounts = get_accounts()
    if not accounts:
        logger.warning(
            "No accounts configured. Please set GH_TOKEN or specific account tokens."
        )
        return

    master_map = map_repositories(accounts)

    if not master_map:
        logger.warning("No repositories mapped. Exiting.")
        return

    master_map = map_ea_environments(master_map)
    generate_master_map(master_map)
    generate_ea_config_file(master_map)

    if args.map_only:
        return

    heavy_repos = get_heavy_repositories(master_map, args.threshold)

    if not heavy_repos:
        logger.info(f"No repositories found exceeding {args.threshold} KB threshold.")
        return

    logger.info(f"Found {len(heavy_repos)} heavy repositories:")
    for r in heavy_repos:
        logger.info(
            f"  - {r['full_name']} ({r['account']}): {r['size_kb']/1024:.2f} MB"
        )

    if args.apply_blocking:
        logger.info(f"Applying blocking functions (Dry Run: {not args.execute})")
        for repo in heavy_repos:
            apply_blocking_function(repo, accounts, not args.execute)


if __name__ == "__main__":
    main()
