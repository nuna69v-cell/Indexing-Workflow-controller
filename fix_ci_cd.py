import re

with open(".github/workflows/ci-cd.yml", "r") as f:
    content = f.read()

replacement = """        export TA_INCLUDE_PATH=/usr/include/ta-lib
        export TA_LIBRARY_PATH=/usr/lib
        export LDFLAGS="-L/usr/lib"
        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock"""

content = re.sub(
    r'        export TA_INCLUDE_PATH=/usr/include/ta-lib\n        export TA_LIBRARY_PATH=/usr/lib\n        export LDFLAGS="-L/usr/lib"\n        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock',
    replacement,
    content
)

with open(".github/workflows/ci-cd.yml", "w") as f:
    f.write(content)
