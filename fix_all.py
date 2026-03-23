import re

for filename in [".github/workflows/ci-cd.yml", ".github/workflows/ci.yml"]:
    with open(filename, "r") as f:
        content = f.read()

    content = content.replace(
        'pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader',
        'pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn',
    )
    content = content.replace(
        'pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader',
        'pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn',
    )

    with open(filename, "w") as f:
        f.write(content)
