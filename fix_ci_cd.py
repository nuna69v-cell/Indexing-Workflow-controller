with open('.github/workflows/ci-cd.yml', 'r') as f:
    content = f.read()

content = content.replace('''    - name: Install dependencies
      run: \'python -m pip install --upgrade pip

        pip install -r requirements.txt

        export TA_INCLUDE_PATH=/usr/include/ta-lib
        export TA_LIBRARY_PATH=/usr/lib
        export LDFLAGS="-L/usr/lib"
        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock

        \'''', '''    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        export TA_INCLUDE_PATH=/usr/include/ta-lib
        export TA_LIBRARY_PATH=/usr/lib
        export LDFLAGS="-L/usr/lib"
        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock
''')

with open('.github/workflows/ci-cd.yml', 'w') as f:
    f.write(content)
