import subprocess
import os


def run_cmd(cmd):
    print(f"Running: {cmd}")
    env = os.environ.copy()
    env["TA_INCLUDE_PATH"] = "/usr/include/ta-lib"
    env["TA_LIBRARY_PATH"] = "/usr/lib"
    env["LDFLAGS"] = "-L/usr/lib"
    env["LD_LIBRARY_PATH"] = "/usr/lib:" + env.get("LD_LIBRARY_PATH", "")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


run_cmd(".venv/bin/pip install -r requirements.txt")
