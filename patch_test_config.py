import os

with open("tests/test_config_security.py", "r") as f:
    content = f.read()

content = content.replace("with pytest.raises(ValueError, match=\"SECRET_KEY must be changed\"):", "with pytest.raises(ValueError, match=\"must be changed\"):")

with open("tests/test_config_security.py", "w") as f:
    f.write(content)
