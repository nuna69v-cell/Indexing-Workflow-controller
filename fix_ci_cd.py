import re

with open(".github/workflows/ci-cd.yml", "r") as f:
    content = f.read()

# Fix multi-line run formatting for dependencies
content = content.replace("      run: 'python -m pip install --upgrade pip\n\n        pip install -r requirements.txt\n\n        export TA_INCLUDE_PATH=/usr/include/ta-lib\n        export TA_LIBRARY_PATH=/usr/lib\n        export LDFLAGS=\"-L/usr/lib\"\n        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock\n\n        '", "      run: |\n        python -m pip install --upgrade pip\n        pip install -r requirements.txt\n        export TA_INCLUDE_PATH=/usr/include/ta-lib\n        export TA_LIBRARY_PATH=/usr/lib\n        export LDFLAGS=\"-L/usr/lib\"\n        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock")

# Fix multi-line run formatting for tests
content = content.replace("      run: 'python -m pytest tests/ -v --cov=. --cov-report=xml --cov-report=html\n\n        '", "      run: |\n        python -m pytest tests/ -v --cov=. --cov-report=xml --cov-report=html")

# Fix multi-line run formatting for lint
content = content.replace("      run: 'pip install black flake8 isort bandit safety mypy\n\n        '", "      run: |\n        pip install black flake8 isort bandit safety mypy")

# Fix multi-line run formatting for Docker build
content = content.replace("          type=raw,value=latest,enable={{is_default_branch}}\n\n          '", "          type=raw,value=latest,enable={{is_default_branch}}")

# Fix multi-line run formatting for Deploy to staging
old_staging = """    - name: Deploy to staging
      env:
        DATABASE_URL: ${{ secrets.DATABASE_URL }}
        REDIS_URL: ${{ secrets.REDIS_URL }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      run: "echo '\\U0001F680 Deploying to staging environment'\\necho 'Image: ${{ needs.build.outputs.image-tag }}'\\necho 'Environment:\\\n        \\ staging'\\n\""""

new_staging = """    - name: Deploy to staging
      env:
        DATABASE_URL: ${{ secrets.DATABASE_URL }}
        REDIS_URL: ${{ secrets.REDIS_URL }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      run: |
        echo '\U0001F680 Deploying to staging environment'
        echo 'Image: ${{ needs.build.outputs.image-tag }}'
        echo 'Environment: staging'"""

# Fix multi-line run formatting for Deploy to production
old_prod = """    - name: Deploy to production
      env:
        DATABASE_URL: ${{ secrets.DATABASE_URL }}
        REDIS_URL: ${{ secrets.REDIS_URL }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        BYBIT_API_KEY: ${{ secrets.BYBIT_API_KEY }}
        BYBIT_API_SECRET: ${{ secrets.BYBIT_API_SECRET }}
        FXCM_API_TOKEN: ${{ secrets.FXCM_API_TOKEN }}
      run: "echo '\\U0001F680 Deploying to production environment'\\necho 'Image: ${{ needs.build.outputs.image-tag }}'\\necho\\\n        \\ 'Environment: production'\\necho '\\u2705 Production deployment completed'\\n\"\n    - name: Health check\n      run: \"echo '\\U0001F3E5 Running health checks...'\\necho '\\u2705 All services healthy'\\n\""""

new_prod = """    - name: Deploy to production
      env:
        DATABASE_URL: ${{ secrets.DATABASE_URL }}
        REDIS_URL: ${{ secrets.REDIS_URL }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        BYBIT_API_KEY: ${{ secrets.BYBIT_API_KEY }}
        BYBIT_API_SECRET: ${{ secrets.BYBIT_API_SECRET }}
        FXCM_API_TOKEN: ${{ secrets.FXCM_API_TOKEN }}
      run: |
        echo '\U0001F680 Deploying to production environment'
        echo 'Image: ${{ needs.build.outputs.image-tag }}'
        echo 'Environment: production'
        echo '\u2705 Production deployment completed'
    - name: Health check
      run: |
        echo '\U0001F3E5 Running health checks...'
        echo '\u2705 All services healthy'"""

content = content.replace(old_staging, new_staging)
content = content.replace(old_prod, new_prod)

with open(".github/workflows/ci-cd.yml", "w") as f:
    f.write(content)
