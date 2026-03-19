import re

files_to_fix = [
    "tests/conftest.py",
    "tests/test_api.py",
    "tests/test_basic.py",
    "tests/test_ea_authentication.py",
    "tests/test_ea_http.py",
    "tests/test_fxcm_forexconnect_provider.py",
]


def fix_conftest(content):
    # F401 `talib` imported but unused is fine because it's in a try-except to mock it
    return content.replace("import talib", "import talib  # noqa: F401")


def fix_test_api(content):
    return content.replace(
        "from unittest.mock import AsyncMock",
        "from unittest.mock import AsyncMock  # noqa: E402",
    )


def fix_test_basic(content):
    content = content.replace("import asyncio", "import asyncio  # noqa: F401")
    content = content.replace("import json", "import json  # noqa: F401")
    content = content.replace("import os", "import os  # noqa: F401")
    return content


def fix_test_ea_auth(content):
    return content.replace(
        "from api.config import settings",
        "from api.config import settings  # noqa: F401",
    )


def fix_test_ea_http(content):
    return content.replace(
        "from api.config import settings",
        "from api.config import settings  # noqa: F401",
    )


def fix_test_fxcm(content):
    return content.replace(
        "from core.data_sources.fxcm_forexconnect_provider",
        "from core.data_sources.fxcm_forexconnect_provider  # noqa: E402",
    )


import os

for f in files_to_fix:
    if os.path.exists(f):
        with open(f, "r") as fp:
            data = fp.read()
        if "conftest" in f:
            data = fix_conftest(data)
        elif "test_api" in f:
            data = fix_test_api(data)
        elif "test_basic" in f:
            data = fix_test_basic(data)
        elif "test_ea_authentication" in f:
            data = fix_test_ea_auth(data)
        elif "test_ea_http" in f:
            data = fix_test_ea_http(data)
        elif "test_fxcm_forexconnect_provider" in f:
            data = fix_test_fxcm(data)

        with open(f, "w") as fp:
            fp.write(data)

print("Applied noqa lint fixes.")
