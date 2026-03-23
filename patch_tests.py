import re

with open("tests/conftest.py", "r") as f:
    content = f.read()

content = content.replace("    import talib\n", "    import talib  # noqa: F401\n")
with open("tests/conftest.py", "w") as f:
    f.write(content)

with open("tests/test_api.py", "r") as f:
    content = f.read()

content = content.replace("from unittest.mock import AsyncMock\n", "from unittest.mock import AsyncMock  # noqa: E402\n")
with open("tests/test_api.py", "w") as f:
    f.write(content)

with open("tests/test_fxcm_forexconnect_provider.py", "r") as f:
    content = f.read()

content = content.replace("from core.data_sources.fxcm_forexconnect_provider import (\n", "from core.data_sources.fxcm_forexconnect_provider import (  # noqa: E402\n")
with open("tests/test_fxcm_forexconnect_provider.py", "w") as f:
    f.write(content)
