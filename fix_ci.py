import os

files_to_fix = [
    ".github/workflows/ci.yml",
    ".github/workflows/ci-cd.yml",
    ".github/workflows/copilot-setup-steps.yml",
]

for file in files_to_fix:
    if not os.path.exists(file):
        continue
    with open(file, "r") as f:
        content = f.read()

    # Apply inline exports for TA-Lib compilation
    # Handle `pip install -r requirements.txt`
    content = content.replace(
        "if [ -f requirements.txt ]; then pip install -r requirements.txt; fi",
        'if [ -f requirements.txt ]; then TA_INCLUDE_PATH=/usr/include/ta-lib TA_LIBRARY_PATH=/usr/lib LDFLAGS="-L/usr/lib" pip install -r requirements.txt; fi',
    )
    # Remove standalone export commands causing issues
    lines = content.split("\n")
    filtered = []
    for line in lines:
        if line.strip().startswith(
            "export TA_INCLUDE_PATH="
        ) and not line.strip().startswith("if ["):
            continue
        if line.strip().startswith("export TA_LIBRARY_PATH="):
            continue
        if line.strip().startswith("export LDFLAGS="):
            continue
        filtered.append(line)

    content = "\n".join(filtered)

    # Handle `pip install pytest...`
    content = content.replace(
        "pip install ruff pytest pytest-cov",
        'TA_INCLUDE_PATH=/usr/include/ta-lib TA_LIBRARY_PATH=/usr/lib LDFLAGS="-L/usr/lib" pip install ruff pytest pytest-cov',
    )
    content = content.replace(
        "pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock",
        'TA_INCLUDE_PATH=/usr/include/ta-lib TA_LIBRARY_PATH=/usr/lib LDFLAGS="-L/usr/lib" pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock',
    )

    with open(file, "w") as f:
        f.write(content)

print("Fixed CI files.")
