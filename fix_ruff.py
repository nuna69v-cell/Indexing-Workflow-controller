import re

def fix_file(filepath, patterns):
    with open(filepath, "r") as f:
        content = f.read()

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    with open(filepath, "w") as f:
        f.write(content)

fix_file("tests/conftest.py", [
    (r"import talib", r"import talib  # noqa: F401")
])

fix_file("tests/test_api.py", [
    (r"from unittest\.mock import AsyncMock", r"from unittest.mock import AsyncMock  # noqa: E402")
])

fix_file("tests/test_basic.py", [
    (r"import asyncio\n        import json\n        import os", r"import asyncio  # noqa: F401\n        import json  # noqa: F401\n        import os  # noqa: F401")
])

fix_file("tests/test_ea_authentication.py", [
    (r"from api\.config import settings", r"from api.config import settings  # noqa: F401")
])

fix_file("tests/test_ea_http.py", [
    (r"from api\.config import settings", r"from api.config import settings  # noqa: F401")
])

fix_file("tests/test_fxcm_credentials_removed.py", [
    (r"except:", r"except Exception:")
])

fix_file("tests/test_fxcm_forexconnect_provider.py", [
    (r"from core\.data_sources\.fxcm_forexconnect_provider import \(", r"from core.data_sources.fxcm_forexconnect_provider import (  # noqa: E402")
])
