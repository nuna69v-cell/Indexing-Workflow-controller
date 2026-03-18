import re

with open("Indexing-Workflow-controller/tests/conftest.py", "r") as f:
    content = f.read()

content = content.replace("ea_http.pending_signals = []", "from collections import deque\n        ea_http.pending_signals = deque()")

with open("Indexing-Workflow-controller/tests/conftest.py", "w") as f:
    f.write(content)
