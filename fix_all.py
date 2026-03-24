for filename in [".github/workflows/ci-cd.yml", ".github/workflows/ci.yml"]:
    with open(filename, "r") as f:
        content = f.read()

    content = content.replace(
        'pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn',
        'pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn openpyxl',
    )
    content = content.replace(
        'pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn',
        'pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn openpyxl',
    )

    with open(filename, "w") as f:
        f.write(content)
