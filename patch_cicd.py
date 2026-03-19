import re

with open(".github/workflows/ci-cd.yml", "r") as f:
    content = f.read()

# Replace the specific chunk
old_chunk = """    - name: Install dependencies
      run: 'python -m pip install --upgrade pip

        pip install -r requirements.txt

        export TA_INCLUDE_PATH=/usr/include/ta-lib
        export TA_LIBRARY_PATH=/usr/lib
        export LDFLAGS="-L/usr/lib"
        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock

        '"""

new_chunk = """    - name: Install dependencies
      env:
        TA_INCLUDE_PATH: /usr/include/ta-lib
        TA_LIBRARY_PATH: /usr/lib
        LDFLAGS: "-L/usr/lib"
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock"""

if old_chunk in content:
    content = content.replace(old_chunk, new_chunk)
    with open(".github/workflows/ci-cd.yml", "w") as f:
        f.write(content)
    print("Successfully patched ci-cd.yml")
else:
    print("Could not find the chunk to replace in ci-cd.yml")
