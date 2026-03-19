import subprocess
import sys


def run_git_push():
    try:
        result = subprocess.run(
            ["git", "push", "origin", "jules-1585480126304078704-14cfa217"],
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)


if __name__ == "__main__":
    run_git_push()
