with open(".github/workflows/ci.yml", "r") as f:
    content = f.read()

import re

# wrap long pip install line
content = re.sub(
    r'pip install ruff pytest pytest-cov pytest-asyncio pytest-mock fastapi backtrader numpy pandas redis scikit-learn joblib psutil pydantic-settings supabase praw cryptography httpx scipy aiohttp pybit',
    r'pip install ruff pytest pytest-cov pytest-asyncio pytest-mock \\\n            fastapi backtrader numpy pandas redis scikit-learn joblib \\\n            psutil pydantic-settings supabase praw cryptography httpx \\\n            scipy aiohttp pybit',
    content
)

with open(".github/workflows/ci.yml", "w") as f:
    f.write(content)

with open(".github/workflows/ci-cd.yml", "r") as f:
    content = f.read()

content = re.sub(
    r'pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock fastapi backtrader numpy pandas redis scikit-learn joblib psutil pydantic-settings supabase praw cryptography scipy aiohttp',
    r'pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock \\\n          fastapi backtrader numpy pandas redis scikit-learn joblib \\\n          psutil pydantic-settings supabase praw cryptography scipy aiohttp',
    content
)

with open(".github/workflows/ci-cd.yml", "w") as f:
    f.write(content)
