import subprocess
import sys


def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


run_cmd("python -m venv .venv")
run_cmd(".venv/bin/pip install -r requirements.txt")
