import subprocess
import os

if __name__ == "__main__":
    print("Running setup-exness-vps.sh locally...")
    # Add execute permission
    os.chmod("deploy/setup-exness-vps.sh", 0o755)

    # Run the script and write output directly to stdout
    process = subprocess.Popen(
        ["bash", "deploy/setup-exness-vps.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    for line in iter(process.stdout.readline, ""):
        print(line, end="")

    process.stdout.close()
    return_code = process.wait()
    print(f"\nReturn code: {return_code}")
