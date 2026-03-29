for filename in [".github/workflows/ci-cd.yml", ".github/workflows/ci.yml"]:
    with open(filename, "r") as f:
        content = f.read()

    content = content.replace(
        'pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn openpyxl',
        'pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn openpyxl python-dotenv requests sqlalchemy',
    )
    content = content.replace(
        'pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn openpyxl',
        'pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn openpyxl python-dotenv requests sqlalchemy',
    )

    with open(filename, "w") as f:
        f.write(content)
