#!/bin/bash
sed -i "s/    - name: Install dependencies\n      run: 'python -m pip install --upgrade pip\n\n        pip install -r requirements.txt\n\n        export TA_INCLUDE_PATH=\/usr\/include\/ta-lib\n        export TA_LIBRARY_PATH=\/usr\/lib\n        export LDFLAGS=\"-L\/usr\/lib\"\n        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock\n\n        '/    - name: Install dependencies\n      run: |\n        python -m pip install --upgrade pip\n        pip install -r requirements.txt\n        export TA_INCLUDE_PATH=\/usr\/include\n        export TA_LIBRARY_PATH=\/usr\/lib\n        export LDFLAGS=\"-L\/usr\/lib\"\n        pip install pytest pytest-cov pytest-asyncio httpx pybit pytest-mock/" .github/workflows/ci-cd.yml

sed -i "s/      run: 'python -m pytest tests\/ -v --cov=. --cov-report=xml --cov-report=html\n\n        '/      run: |\n        python -m pytest tests\/ -v --cov=. --cov-report=xml --cov-report=html/" .github/workflows/ci-cd.yml

sed -i "s/      run: 'pip install black flake8 isort bandit safety mypy\n\n        '/      run: |\n        pip install black flake8 isort bandit safety mypy/" .github/workflows/ci-cd.yml

sed -i "s/        tags: 'type=ref,event=branch\n\n          type=ref,event=pr\n\n          type=sha,prefix={{branch}}-\n\n          type=raw,value=latest,enable={{is_default_branch}}\n\n          /        tags: |\n          type=ref,event=branch\n          type=ref,event=pr\n          type=sha,prefix={{branch}}-\n          type=raw,value=latest,enable={{is_default_branch}}/" .github/workflows/ci-cd.yml

sed -i "s/      run: \"echo '\\\\U0001F680 Deploying to staging environment'\\\\necho 'Image: \${{ needs.build.outputs.image-tag }}'\\\\necho 'Environment:\\\\\n        \\\\ staging'\\\\n\"/      run: |\n        echo '\\\\U0001F680 Deploying to staging environment'\n        echo 'Image: \${{ needs.build.outputs.image-tag }}'\n        echo 'Environment: staging'/" .github/workflows/ci-cd.yml

sed -i "s/      run: \"echo '\\\\U0001F680 Deploying to production environment'\\\\necho 'Image: \${{ needs.build.outputs.image-tag }}'\\\\necho 'Environment:\\\\\n        \\\\ production'\\\\n\"/      run: |\n        echo '\\\\U0001F680 Deploying to production environment'\n        echo 'Image: \${{ needs.build.outputs.image-tag }}'\n        echo 'Environment: production'/" .github/workflows/ci-cd.yml
