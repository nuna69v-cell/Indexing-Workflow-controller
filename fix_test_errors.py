import sys
from unittest.mock import patch, MagicMock, AsyncMock

# Fix for conftest.py
with open("tests/conftest.py", "r") as f:
    content = f.read()

content = content.replace("import talib", "import talib  # noqa: F401")
with open("tests/conftest.py", "w") as f:
    f.write(content)

# Fix for test_api.py
with open("tests/test_api.py", "r") as f:
    content = f.read()

# E402 Module level import not at top of file
lines = content.split("\n")
for i, line in enumerate(lines):
    if line.startswith("from unittest.mock import AsyncMock"):
        lines.pop(i)
        lines.insert(0, line)
        break

with open("tests/test_api.py", "w") as f:
    f.write("\n".join(lines))

# Fix for test_basic.py
with open("tests/test_basic.py", "r") as f:
    content = f.read()

content = content.replace("import asyncio", "import asyncio  # noqa: F401")
content = content.replace("import json", "import json  # noqa: F401")
content = content.replace("import os", "import os  # noqa: F401")

with open("tests/test_basic.py", "w") as f:
    f.write(content)

# Fix for test_config_security.py
with open("tests/test_config_security.py", "r") as f:
    content = f.read()

content = content.replace("settings = Settings()", "_ = Settings()")

with open("tests/test_config_security.py", "w") as f:
    f.write(content)

# Fix for test_ea_authentication.py
with open("tests/test_ea_authentication.py", "r") as f:
    content = f.read()

content = content.replace("from api.config import settings", "")
with open("tests/test_ea_authentication.py", "w") as f:
    f.write(content)

# Fix for test_ea_http.py
with open("tests/test_ea_http.py", "r") as f:
    content = f.read()

content = content.replace("from api.config import settings", "")
with open("tests/test_ea_http.py", "w") as f:
    f.write(content)

# Fix for test_fxcm_credentials_removed.py
with open("tests/test_fxcm_credentials_removed.py", "r") as f:
    content = f.read()

content = content.replace("except:\n", "except Exception:\n")
with open("tests/test_fxcm_credentials_removed.py", "w") as f:
    f.write(content)

# Fix for test_fxcm_forexconnect_provider.py
with open("tests/test_fxcm_forexconnect_provider.py", "r") as f:
    content = f.read()

lines = content.split("\n")
start_idx = -1
end_idx = -1
import_block = []
for i, line in enumerate(lines):
    if line.startswith("from core.data_sources.fxcm_forexconnect_provider import ("):
        start_idx = i
        import_block.append(line)
    elif start_idx != -1 and line == ")":
        end_idx = i
        import_block.append(line)
        break
    elif start_idx != -1:
        import_block.append(line)

if start_idx != -1 and end_idx != -1:
    # Delete the old import block
    del lines[start_idx : end_idx + 1]

    # Insert it at the top after other imports
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("import") or line.startswith("from"):
            insert_idx = i + 1

    for i, imp_line in enumerate(import_block):
        lines.insert(insert_idx + i, imp_line)

with open("tests/test_fxcm_forexconnect_provider.py", "w") as f:
    f.write("\n".join(lines))
