import re

def update_workflow(filename):
    with open(filename, "r") as f:
        content = f.read()

    # In ci-cd.yml and ci.yml we need to add the missing dependencies.
    # We added pytest-asyncio httpx pybit pytest-mock but we also need
    # fastapi pydantic-settings joblib backtrader aiohttp

    new_content = re.sub(
        r"pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock",
        r"pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings joblib backtrader aiohttp",
        content
    )

    # Also update the ruff install command in ci.yml just in case it's used there
    new_content = re.sub(
        r"pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock",
        r"pip install ruff pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi pydantic-settings joblib backtrader aiohttp",
        new_content
    )

    with open(filename, "w") as f:
        f.write(new_content)

update_workflow(".github/workflows/ci.yml")
update_workflow(".github/workflows/ci-cd.yml")
