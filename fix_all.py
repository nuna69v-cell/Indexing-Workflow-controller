for filename in [".github/workflows/ci-cd.yml", ".github/workflows/ci.yml"]:
    with open(filename, "r") as f:
        content = f.read()

    content = content.replace(
        'export LDFLAGS="-L/usr/lib"\n          pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn',
        'export LDFLAGS="-L/usr/lib"\n        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings cryptography joblib backtrader redis scikit-learn'
    )

    with open(filename, "w") as f:
        f.write(content)
