with open("tests/test_fxcm_forexconnect_provider.py", "r") as f:
    content = f.read()

content = content.replace(
    "from core.data_sources.fxcm_forexconnect_provider  # noqa: E402 import (",
    "from core.data_sources.fxcm_forexconnect_provider import (  # noqa: E402",
)

with open("tests/test_fxcm_forexconnect_provider.py", "w") as f:
    f.write(content)
