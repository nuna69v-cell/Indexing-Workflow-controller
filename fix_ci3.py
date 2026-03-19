with open('.github/workflows/ci-cd.yml', 'r') as f:
    c = f.read()

c = c.replace("""        export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
        export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
        python -m pytest tests/ -v --cov=. --cov-report=xml --cov-report=html""", """        export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
        python -m pytest tests/ -v --cov=. --cov-report=xml --cov-report=html""")

with open('.github/workflows/ci-cd.yml', 'w') as f:
    f.write(c)
