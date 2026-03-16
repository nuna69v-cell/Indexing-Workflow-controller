import requests
import json
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Tokens from your .env
TOKENS = {
    "mouyleng172": os.getenv("GH_USER_TOKEN"),
    "LengKundee": os.getenv("GH_TOKEN")
}

def get_repo_map():
    master_map = {}

    for user, token in TOKENS.items():
        if not token:
            print(f"Warning: No token found for {user}. Skipping.")
            continue

        print(f"Mapping repositories for: {user}...")
        url = f"https://api.github.com/users/{user}/repos"
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = response.json()
            master_map[user] = [
                {
                    "name": r["name"],
                    "url": r["clone_url"],
                    "branch": r["default_branch"],
                    "description": r["description"]
                } for r in repos
            ]
        else:
            print(f"Failed to fetch {user}: {response.status_code} - {response.text}")

    with open(".master-map.json", "w") as f:
        json.dump(master_map, f, indent=4)
    print("Master Map created successfully!")

def clone_or_pull_repos():
    if not os.path.exists(".master-map.json"):
        print("Master map not found. Run get_repo_map() first.")
        return

    with open(".master-map.json", "r") as f:
        master_map = json.load(f)

    for user, repos in master_map.items():
        user_dir = f"Accounts/{user}"
        os.makedirs(user_dir, exist_ok=True)

        for repo in repos:
            repo_name = repo["name"]
            repo_url = repo["url"]
            repo_path = os.path.join(user_dir, repo_name)

            print(f"\nProcessing {user}/{repo_name}...")

            if os.path.exists(repo_path):
                print(f"Directory {repo_path} exists. Attempting git pull...")
                try:
                    # In a real setup you might want to fetch and check status instead of a direct pull
                    # to avoid merge conflicts on active branches
                    subprocess.run(["git", "-C", repo_path, "fetch"], check=True)
                    subprocess.run(["git", "-C", repo_path, "status", "-s"], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error checking {repo_name}: {e}")
            else:
                print(f"Cloning {repo_name}...")
                try:
                    subprocess.run(["git", "clone", repo_url, repo_path], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error cloning {repo_name}: {e}")

if __name__ == "__main__":
    print("Starting GitHub Repository Maintenance...")
    get_repo_map()
    print("Map generated. Run clone_or_pull_repos() to sync.")
    # Uncomment to automatically sync
    # clone_or_pull_repos()
