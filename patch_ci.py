import re

with open(".github/workflows/ci.yml", "r") as f:
    content = f.read()

# Replace the specific chunk
old_chunk = """        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          export TA_INCLUDE_PATH=/usr/include/ta-lib
          export TA_LIBRARY_PATH=/usr/lib
          export LDFLAGS="-L/usr/lib"
          pip install ruff pytest pytest-cov"""

new_chunk = """        env:
          TA_INCLUDE_PATH: /usr/include/ta-lib
          TA_LIBRARY_PATH: /usr/lib
          LDFLAGS: "-L/usr/lib"
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install ruff pytest pytest-cov"""

if old_chunk in content:
    content = content.replace(old_chunk, new_chunk)
    with open(".github/workflows/ci.yml", "w") as f:
        f.write(content)
    print("Successfully patched ci.yml")
else:
    print("Could not find the chunk to replace in ci.yml")
