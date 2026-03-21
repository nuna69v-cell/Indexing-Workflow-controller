#!/usr/bin/env python3
"""
Forgejo Migration Script
Automates cloning and migrating repositories to Forgejo (forge.mql5.io).
Reference: https://replit.com/@Meizhuxie4/Forgejo-Mugration
"""

import os
import subprocess
import sys
import argparse


def run_command(command, description):
    print(f"🚀 {description}...")
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        return False


def migrate(source_url, dest_url, token=None):
    print(f"🔄 Starting migration from {source_url} to {dest_url}")

    # 1. Prepare destination URL with token if provided
    if token and "://" in dest_url:
        protocol, rest = dest_url.split("://")
        # Handle case where dest_url might already have a user
        if "@" in rest:
            _, host_path = rest.split("@")
            authenticated_dest = f"{protocol}://{token}@{host_path}"
        else:
            authenticated_dest = f"{protocol}://{token}@{rest}"
    else:
        authenticated_dest = dest_url

    # 2. Add remote or update existing
    if not os.path.exists(".git"):
        print("📁 Not a git repository. Cloning source first...")
        if not run_command(
            f"git clone --mirror {source_url} migration_temp", "Cloning source mirror"
        ):
            return
        os.chdir("migration_temp")
    else:
        print("✅ Current directory is a git repository.")

    # 3. Push to destination
    print("📤 Pushing to Forgejo...")
    run_command(
        f"git push --mirror {authenticated_dest}", "Pushing to Forgejo destination"
    )

    print("✅ Migration process finished.")


def main():
    parser = argparse.ArgumentParser(description="Forgejo Migration Tool")
    parser.add_argument(
        "--source",
        help="Source repository URL",
        default="https://github.com/A6-9V/A6..9V-GenX_FX.git",
    )
    parser.add_argument(
        "--dest",
        help="Destination Forgejo URL",
        default="https://forge.mql5.io/A6-9V/GenX_FX.git",
    )
    parser.add_argument(
        "--token", help="Forgejo Access Token", default=os.getenv("FORGE_ACCESS_TOKEN")
    )

    args = parser.parse_args()

    if not args.dest:
        print("❌ Error: Destination URL is required.")
        sys.exit(1)

    migrate(args.source, args.dest, args.token)


if __name__ == "__main__":
    main()
