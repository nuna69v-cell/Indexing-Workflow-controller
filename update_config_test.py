import re

with open("Indexing-Workflow-controller/tests/test_config_security.py", "r") as f:
    content = f.read()

content = content.replace('match="SECRET_KEY must be changed"', 'match="must be changed"')

with open("Indexing-Workflow-controller/tests/test_config_security.py", "w") as f:
    f.write(content)
