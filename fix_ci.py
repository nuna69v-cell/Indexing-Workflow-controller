import os

files = ['.github/workflows/ci-cd.yml', '.github/workflows/ci.yml', '.github/workflows/copilot-setup-steps.yml']

for filepath in files:
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Upgrade deprecated actions
    content = content.replace("actions/checkout@v3", "actions/checkout@v4")
    content = content.replace("actions/setup-python@v4", "actions/setup-python@v5")
    content = content.replace("actions/cache@v3", "actions/cache@v4")
    content = content.replace("codecov/codecov-action@v3", "codecov/codecov-action@v4")

    # 2. Add TA-Lib installation script replacement for CI.yml and CI-CD.yml
    if "sudo apt-get install -y libopenblas-dev" in content:
        # Replacement for ci-cd.yml
        old_block = """        sudo apt-get update
        sudo apt-get install -y libopenblas-dev
        if [ -f ta-lib/ta-lib_0.6.4_amd64.deb ]; then
          sudo dpkg -i ta-lib/ta-lib_0.6.4_amd64.deb || sudo apt-get install -f -y
          sudo ln -s /usr/lib/libta-lib.so /usr/lib/libta_lib.so || true
        fi"""
        new_block = """        sudo apt-get update
        sudo apt-get install -y build-essential wget libopenblas-dev
        wget https://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
        tar -xzf ta-lib-0.4.0-src.tar.gz
        cd ta-lib
        ./configure --prefix=/usr
        make
        sudo make install
        cd ..
        rm -rf ta-lib ta-lib-0.4.0-src.tar.gz"""
        content = content.replace(old_block, new_block)

    # Replace inline pip exports in ci-cd.yml
    old_pip = """        export TA_INCLUDE_PATH=/usr/include/ta-lib
        export TA_LIBRARY_PATH=/usr/lib
        export LDFLAGS="-L/usr/lib"
        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock"""
    new_pip = """        export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
        TA_INCLUDE_PATH=/usr/include/ta-lib TA_LIBRARY_PATH=/usr/lib LDFLAGS="-L/usr/lib" pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock"""
    content = content.replace(old_pip, new_pip)

    # In ci.yml
    old_pip_ci = """          export TA_INCLUDE_PATH=/usr/include/ta-lib
          export TA_LIBRARY_PATH=/usr/lib
          export LDFLAGS="-L/usr/lib"
          pip install ruff pytest pytest-cov"""
    new_pip_ci = """          export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
          TA_INCLUDE_PATH=/usr/include/ta-lib TA_LIBRARY_PATH=/usr/lib LDFLAGS="-L/usr/lib" pip install ruff pytest pytest-cov"""
    content = content.replace(old_pip_ci, new_pip_ci)

    # In copilot-setup-steps.yml
    if 'copilot' in filepath:
        content = content.replace("sudo apt-get install -y sqlite3",
                                  "sudo apt-get install -y sqlite3 build-essential wget\n          wget https://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz\n          tar -xzf ta-lib-0.4.0-src.tar.gz\n          cd ta-lib\n          ./configure --prefix=/usr\n          make\n          sudo make install\n          cd ..\n          rm -rf ta-lib ta-lib-0.4.0-src.tar.gz")

        content = content.replace("pip install -r requirements.txt",
                                  "TA_INCLUDE_PATH=/usr/include/ta-lib TA_LIBRARY_PATH=/usr/lib LDFLAGS=\"-L/usr/lib\" pip install -r requirements.txt")

    # In ci-cd.yml and ci.yml: export LD_LIBRARY_PATH for pytest
    content = content.replace("python -m pytest tests/ -v", "export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH\n        python -m pytest tests/ -v")
    content = content.replace("PYTHONPATH=. pytest --cov=src/ tests/", "export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH\n          PYTHONPATH=. pytest --cov=src/ tests/")

    # Also update numpy requirement to <2.0.0 during pip install if not explicitly handled (memory specifies this, but requirements.txt probably has it)
    with open(filepath, 'w') as f:
        f.write(content)
