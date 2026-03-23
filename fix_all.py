import re

for filename in ['.github/workflows/ci-cd.yml', '.github/workflows/ci.yml']:
    with open(filename, 'r') as f:
        content = f.read()

    # ensure the pip installs that failed exist in the yaml
    content = content.replace('pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock',
                              'pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader')
    content = content.replace('pip install ruff pytest pytest-cov',
                              'pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader')

    with open(filename, 'w') as f:
        f.write(content)
