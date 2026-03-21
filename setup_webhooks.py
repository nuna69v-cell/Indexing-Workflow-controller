#!/usr/bin/env python3
"""
Forgejo Webhook Setup Script
Automates the creation of webhooks on forge.mql5.io.
Target Repository: https://forge.mql5.io/LengKundee/A6-9V_VL6-N9.git
"""

import os
import requests
import argparse
import sys


def setup_webhook(api_token, repo_owner, repo_name, webhook_url, events=None):
    if events is None:
        events = ["push", "pull_request", "create", "delete"]

    api_url = f"https://forge.mql5.io/api/v1/repos/{repo_owner}/{repo_name}/hooks"
    headers = {
        "Authorization": f"token {api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "type": "gitea",
        "config": {"url": webhook_url, "content_type": "json"},
        "events": events,
        "active": True,
    }

    print(f"🚀 Creating webhook for {repo_owner}/{repo_name}...")
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 201:
            print("✅ Webhook created successfully.")
        else:
            print(
                f"❌ Failed to create webhook: {response.status_code} - {response.text}"
            )
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Forgejo Webhook Tool")
    parser.add_argument(
        "--token", help="Forgejo API Token", default=os.getenv("FORGE_ACCESS_TOKEN")
    )
    parser.add_argument("--owner", help="Repo Owner", default="LengKundee")
    parser.add_argument("--repo", help="Repo Name", default="A6-9V_VL6-N9")
    parser.add_argument("--url", help="Webhook target URL", required=True)

    args = parser.parse_args()

    if not args.token:
        print("❌ Error: FORGE_ACCESS_TOKEN not set.")
        sys.exit(1)

    setup_webhook(args.token, args.owner, args.repo, args.url)


if __name__ == "__main__":
    main()
