import re

with open('.github/workflows/ci-cd.yml', 'r') as f:
    content = f.read()

# Fix pip install multi-line string in test job with exact matching or regex
content = re.sub(
    r"run: 'python -m pip install --upgrade pip\n\n        pip install -r requirements\.txt\n\n\n        export TA_INCLUDE_PATH=/usr/include/ta-lib\n        export TA_LIBRARY_PATH=/usr/lib\n        export LDFLAGS=\"-L/usr/lib\"\n        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock\n\n        '",
    r"""run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        export TA_INCLUDE_PATH=/usr/include/ta-lib
        export TA_LIBRARY_PATH=/usr/lib
        export LDFLAGS="-L/usr/lib"
        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock""",
    content
)

with open('.github/workflows/ci-cd.yml', 'w') as f:
    f.write(content)
