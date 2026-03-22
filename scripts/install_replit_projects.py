#!/usr/bin/env python3
"""
CLI tool to install/download Replit projects or their GitHub counterparts.
Usage:
  python3 scripts/install_replit_projects.py --github-token <YOUR_TOKEN>
  python3 scripts/install_replit_projects.py --replit-sid <YOUR_CONNECT_SID>
"""

import argparse
import urllib.request
import zipfile
import io
import os
import sys
import subprocess

# The URLs provided by the user
REPLIT_URLS = [
    "https://replit.com/@mouy-leng/httpsgithubcomA6-9VMetatrader5EXNESS",
    "https://replit.com/@mouy-leng/Exness-Auto-Trade",
    "https://replit.com/@mouy-leng/httpsmouy-lenggithubioZOLO-A6-9VxNUNA-",
    "https://replit.com/@mouy-leng/Realtek-Network-Info",
    "https://replit.com/@mouy-leng/VPS-Forge"
]

# Known GitHub counterparts for the Replit URLs
GITHUB_MAPPINGS = {
    "httpsgithubcomA6-9VMetatrader5EXNESS": "https://github.com/A6-9V/Metatrader_5_EXNESS.git",
    "Exness-Auto-Trade": "https://github.com/A6-9V/A6..9V-GenX_FX.main.git",
    "httpsmouy-lenggithubioZOLO-A6-9VxNUNA-": "https://github.com/A6-9V/Metatrader_5_EXNESS.git", # or A6..9V-GenX_FX.main.git
    "Realtek-Network-Info": "https://github.com/Mouy-leng/Realtek-Network-Info.git",
    "VPS-Forge": "https://github.com/mouy-leng/VPS-Forge.git"
}

def download_via_replit(url, sid, output_dir="replit_downloads"):
    """Attempt to download a zip file directly from Replit using a valid session ID."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    slug = url.split('/')[-1]
    username = url.split('/')[-2].replace('@', '')
    zip_url = f"https://replit.com/@{username}/{slug}.zip"

    print(f"Downloading {username}/{slug} via Replit...")
    try:
        req = urllib.request.Request(
            zip_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Cookie': f'connect.sid={sid}'
            }
        )
        with urllib.request.urlopen(req) as response:
            data = response.read()
            print(f"  Downloaded zip file: {len(data)} bytes")

            target_dir = os.path.join(output_dir, slug)
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    z.extractall(target_dir)
                print(f"  Successfully extracted to {target_dir}")
                return True
            except zipfile.BadZipFile:
                print("  Failed: Not a valid zip file. Your connect.sid might be invalid or expired.")
                return False
    except urllib.error.URLError as e:
        print(f"  Failed to download: {e}")
        return False

def clone_via_github(slug, token, output_dir="replit_downloads"):
    """Clone the known GitHub counterpart using a personal access token."""
    if slug not in GITHUB_MAPPINGS:
        print(f"No known GitHub mapping for {slug}")
        return False

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    github_url = GITHUB_MAPPINGS[slug]
    target_dir = os.path.join(output_dir, slug)

    # Inject token into the clone URL
    # Format: https://<token>@github.com/...
    auth_url = github_url.replace("https://", f"https://{token}@")

    print(f"Cloning GitHub counterpart for {slug}...")
    try:
        # We use subprocess to hide the token from the output
        result = subprocess.run(
            ["git", "clone", auth_url, target_dir],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  Successfully cloned to {target_dir}")
            return True
        else:
            # Mask token in error message
            error_msg = result.stderr.replace(token, "***")
            print(f"  Failed to clone: {error_msg.strip()}")
            return False
    except Exception as e:
        print(f"  Exception during git clone: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Download Replit projects or their GitHub counterparts.")
    parser.add_argument("--github-token", help="Your GitHub Personal Access Token (classic or fine-grained)")
    parser.add_argument("--replit-sid", help="Your Replit connect.sid cookie value")
    parser.add_argument("--output-dir", default="replit_downloads", help="Directory to save the projects")

    args = parser.parse_args()

    if not args.github_token and not args.replit_sid:
        print("Error: You must provide either --github-token or --replit-sid")
        parser.print_help()
        sys.exit(1)

    print(f"Starting installation of {len(REPLIT_URLS)} projects to '{args.output_dir}'")

    success_count = 0

    for url in REPLIT_URLS:
        slug = url.split('/')[-1]
        print("-" * 50)

        success = False

        # Try GitHub first if token provided
        if args.github_token:
            success = clone_via_github(slug, args.github_token, args.output_dir)

        # Try Replit if GitHub failed/skipped and SID provided
        if not success and args.replit_sid:
            success = download_via_replit(url, args.replit_sid, args.output_dir)

        if success:
            success_count += 1

    print("=" * 50)
    print(f"Finished processing. Successfully installed {success_count} out of {len(REPLIT_URLS)} projects.")

if __name__ == "__main__":
    main()
