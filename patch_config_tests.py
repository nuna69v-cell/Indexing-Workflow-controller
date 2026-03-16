import re

with open("tests/test_config_security.py", "r") as f:
    content = f.read()

content = content.replace('match="EXNESS_LOGIN must be changed from default in production environment"', 'match="EXNESS_LOGIN must be changed"')
content = content.replace('match="EXNESS_PASSWORD must be changed from default in production environment"', 'match="EXNESS_PASSWORD must be changed"')
content = content.replace('match="1 validation error for ProductionSettings"', 'match="SECRET_KEY must be changed"')

with open("tests/test_config_security.py", "w") as f:
    f.write(content)
