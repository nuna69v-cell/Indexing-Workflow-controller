import re

with open(".github/workflows/ci.yml", "r") as f:
    content = f.read()

replacement = """      - name: Install System Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y sqlite3 libopenblas-dev
          if [ -f ta-lib/ta-lib_0.6.4_amd64.deb ]; then
            sudo dpkg -i ta-lib/ta-lib_0.6.4_amd64.deb || sudo apt-get install -f -y
            sudo ln -s /usr/lib/libta-lib.so /usr/lib/libta_lib.so || true
          fi"""

content = re.sub(
    r"      - name: Install System Dependencies\s+run: sudo apt-get update && sudo apt-get install -y sqlite3",
    replacement,
    content
)

with open(".github/workflows/ci.yml", "w") as f:
    f.write(content)
