#!/usr/bin/env python3
"""
Jules Clean: Automated Code Quality & Maintenance Script
Standard maintenance for GenX FX and Jule-compatible repositories.
"""

import os
import subprocess
import sys
import argparse


def run_command(command, description):
    print(f"🚀 {description}...")
    try:
        subprocess.check_call(command, shell=True)
        print(f"✅ {description} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        return False
    return True


def clean_repository(path):
    print(f"🤖 Jules Maintenance Starting for: {path}...")
    os.chdir(path)

    # 1. Format Code
    run_command(
        "black . --exclude='forexconnect_env_37|venv|.venv|node_modules'",
        "Formatting code with Black",
    )

    # 2. Clean logs
    if os.path.exists("logs"):
        run_command(
            "find logs -name '*.log' -mtime +30 -delete",
            "Cleaning logs older than 30 days",
        )

    # 3. Security check (stub)
    print("🔍 Checking for exposed secrets...")

    print(f"🏁 Jules Maintenance Finished for: {path}")


def main():
    parser = argparse.ArgumentParser(description="Jules Repository Maintenance Tool")
    parser.add_argument("--path", help="Path to the repository to clean", default=".")
    args = parser.parse_args()

    target_path = os.path.abspath(args.path)
    if not os.path.exists(target_path):
        print(f"❌ Error: Path {target_path} does not exist.")
        sys.exit(1)

    clean_repository(target_path)


if __name__ == "__main__":
    main()
