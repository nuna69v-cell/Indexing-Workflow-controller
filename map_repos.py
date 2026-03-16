import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Example token structure (these should be in .env)
TOKENS = {
    "mouyleng172": os.getenv("GH_USER_TOKEN"),
    "LengKundee": os.getenv("GH_TOKEN"),
    "nuna69v-cell": os.getenv("GH_TOKEN_V3")
}

def get_repo_map():
    master_map = {}

    for user, token in TOKENS.items():
        if not token:
            print(f"Skipping {user}: No token found.")
            continue

        print(f"Mapping repositories for: {user}...")
        url = f"https://api.github.com/users/{user}/repos"
        headers = {"Authorization": f"token {token}"}

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
            print(f"Failed to fetch {user}: {response.status_code}")

    with open(".master-map.json", "w") as f:
        json.dump(master_map, f, indent=4)
    print("Master Map created successfully!")

if __name__ == "__main__":
    get_repo_map()
