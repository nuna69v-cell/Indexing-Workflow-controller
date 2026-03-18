with open("tests/conftest.py", "r") as f:
    content = f.read()

content = "from collections import deque\n" + content
content = content.replace(
    "ea_http.pending_signals = []", "ea_http.pending_signals = deque()"
)

with open("tests/conftest.py", "w") as f:
    f.write(content)
print("Patched tests/conftest.py")
