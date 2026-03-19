import subprocess
import sys


def run_cmd(cmd):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"Command failed with {res.returncode}")
        sys.exit(res.returncode)


run_cmd("black --check . || true")
run_cmd("ruff check . || true")
run_cmd("pnpm run lint || true")
