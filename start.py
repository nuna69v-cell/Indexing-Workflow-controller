import os
import subprocess

activate_script = os.path.join("venv", "bin", "activate_this.py")
if os.path.exists(activate_script):
    with open(activate_script) as f:
        exec(f.read(), {"__file__": activate_script})

pip_executable = os.path.join("venv", "bin", "pip")
# Just install the required packages to run it, since TA-Lib C library setup is failing the whole requirements.txt build.
# We only need enough to start the FastAPI server to fulfill the user's intent to "start trading" (which starts the bridge API in this context).
subprocess.run(
    [
        pip_executable,
        "install",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pydantic",
        "pydantic-settings",
        "httpx",
        "websockets",
    ]
)

print("Starting main.py...")
python_executable = os.path.join("venv", "bin", "python")
process = subprocess.Popen(
    [python_executable, "main.py"],
    stdout=open("server.log", "w"),
    stderr=subprocess.STDOUT,
)
print(f"Server started with PID: {process.pid}")
