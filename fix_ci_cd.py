import re

with open(".github/workflows/ci-cd.yml", "r") as f:
    content = f.read()

# Replace the single-quoted block with a literal block scalar
new_content = re.sub(
    r"run: 'python -m pip install --upgrade pip\n\n\s*pip install -r requirements\.txt\n\n\s*export TA_INCLUDE_PATH=/usr/include/ta-lib\n\s*export TA_LIBRARY_PATH=/usr/lib\n\s*export LDFLAGS=\"-L/usr/lib\"\n\s*pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock\n\n\s*'",
    """run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        export TA_INCLUDE_PATH=/usr/include/ta-lib
        export TA_LIBRARY_PATH=/usr/lib
        export LDFLAGS="-L/usr/lib"
        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock""",
    content
)

with open(".github/workflows/ci-cd.yml", "w") as f:
    f.write(new_content)
