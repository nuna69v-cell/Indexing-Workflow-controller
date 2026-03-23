import re

def update_workflow(filename):
    with open(filename, "r") as f:
        content = f.read()

    new_content = re.sub(
        r"pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings joblib backtrader aiohttp",
        r"pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings joblib backtrader aiohttp redis scikit-learn",
        content
    )

    new_content = re.sub(
        r"pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings joblib backtrader aiohttp",
        r"pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings joblib backtrader aiohttp redis scikit-learn",
        new_content
    )

    with open(filename, "w") as f:
        f.write(new_content)

update_workflow(".github/workflows/ci.yml")
update_workflow(".github/workflows/ci-cd.yml")
