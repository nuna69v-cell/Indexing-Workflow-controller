with open("tests/test_fxcm_forexconnect_provider.py", "r") as f:
    content = f.read()

old_str = """from core.data_sources.fxcm_forexconnect_provider import (
    FXCMForexConnectProvider,
)"""

new_str = """from core.data_sources.fxcm_forexconnect_provider import (  # noqa: E402
    FXCMForexConnectProvider,
)"""

content = content.replace(old_str, new_str)

with open("tests/test_fxcm_forexconnect_provider.py", "w") as f:
    f.write(content)
