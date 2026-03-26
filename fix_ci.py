import re

with open(".github/workflows/ci.yml", "r") as f:
    content = f.read()

# Replace the single-quoted block with a literal block scalar
new_content = re.sub(
    r"run: \|\n\s*python -m pip install --upgrade pip\n\s*if \[ -f requirements\.txt \]; then pip install -r requirements\.txt; fi\n\s*export TA_INCLUDE_PATH=/usr/include/ta-lib\n\s*export TA_LIBRARY_PATH=/usr/lib\n\s*export LDFLAGS=\"-L/usr/lib\"\n\s*pip install ruff pytest pytest-cov",
    """run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          export TA_INCLUDE_PATH=/usr/include/ta-lib
          export TA_LIBRARY_PATH=/usr/lib
          export LDFLAGS="-L/usr/lib"
          pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock""",
    content
)

with open(".github/workflows/ci.yml", "w") as f:
    f.write(new_content)
