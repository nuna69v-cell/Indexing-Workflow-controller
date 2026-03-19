import re

with open(".github/workflows/copilot-setup-steps.yml", "r") as f:
    content = f.read()

replacement = """      - name: Install System Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y sqlite3 libopenblas-dev
          if [ -f ta-lib/ta-lib_0.6.4_amd64.deb ]; then
            sudo dpkg -i ta-lib/ta-lib_0.6.4_amd64.deb || sudo apt-get install -f -y
            sudo ln -s /usr/lib/libta-lib.so /usr/lib/libta_lib.so || true
          fi

      - name: Install Python Dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          export TA_INCLUDE_PATH=/usr/include/ta-lib
          export TA_LIBRARY_PATH=/usr/lib
          export LDFLAGS="-L/usr/lib"
          pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock"""

content = re.sub(
    r"      - name: Install System Dependencies\n        run: \|\n          sudo apt-get update\n          sudo apt-get install -y sqlite3\n\n      - name: Install Python Dependencies\n        run: \|\n          python -m pip install --upgrade pip\n          if \[ -f requirements.txt \]; then pip install -r requirements.txt; fi",
    replacement,
    content
)

with open(".github/workflows/copilot-setup-steps.yml", "w") as f:
    f.write(content)
