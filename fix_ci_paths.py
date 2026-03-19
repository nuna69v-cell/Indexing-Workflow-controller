import os

files = ['.github/workflows/ci-cd.yml', '.github/workflows/ci.yml', '.github/workflows/copilot-setup-steps.yml']

for filepath in files:
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r') as f:
        content = f.read()

    # Revert TA_INCLUDE_PATH=/usr/include back to TA_INCLUDE_PATH=/usr/include/ta-lib
    content = content.replace("TA_INCLUDE_PATH=/usr/include TA_LIBRARY_PATH=/usr/lib", "TA_INCLUDE_PATH=/usr/include/ta-lib TA_LIBRARY_PATH=/usr/lib")

    with open(filepath, 'w') as f:
        f.write(content)
