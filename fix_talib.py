import sys

with open("tests/conftest.py", "r") as f:
    content = f.read()

content = content.replace('TA_FUNC_FLAGS = {}', 'TA_FUNC_FLAGS = {}\n        TA_OUTPUT_FLAGS = {}\n        TA_INPUT_FLAGS = {}\n        TA_OPT_INPUT_FLAGS = {}')

with open("tests/conftest.py", "w") as f:
    f.write(content)
