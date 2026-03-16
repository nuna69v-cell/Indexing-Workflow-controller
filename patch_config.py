import re

with open("api/config.py", "r") as f:
    content = f.read()

# Revert ProductionSettings changes
content = re.sub(
    r'@model_validator\(mode="after"\)\n\s+def validate_production_security\(self\) -> "ProductionSettings":.*?return self',
    """@model_validator(mode="after")
    def validate_production_security(self) -> "ProductionSettings":
        if getattr(self, "SECRET_KEY", "default_secret_key") == "default_secret_key" or getattr(self, "SECRET_KEY") == "test_secret_key_12345":
            raise ValueError("SECRET_KEY must be changed")
        if getattr(self, "EXNESS_LOGIN", "default_login") == "default_login":
            raise ValueError("EXNESS_LOGIN must be changed")
        if getattr(self, "EXNESS_PASSWORD", "default_password") == "default_password":
            raise ValueError("EXNESS_PASSWORD must be changed")
        return self""",
    content,
    flags=re.DOTALL
)

with open("api/config.py", "w") as f:
    f.write(content)
