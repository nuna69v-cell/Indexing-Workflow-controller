with open(".github/workflows/ci-cd.yml", "r") as f:
    content = f.read()

# Let's fix the multi-line tags for Extract metadata correctly
import re

content = re.sub(
    r"tags: 'type=ref,event=branch\n\n          type=ref,event=pr\n\n          type=sha,prefix={{branch}}-\n\n          type=raw,value=latest,enable={{is_default_branch}}",
    "tags: |\n          type=ref,event=branch\n          type=ref,event=pr\n          type=sha,prefix={{branch}}-\n          type=raw,value=latest,enable={{is_default_branch}}",
    content
)

with open(".github/workflows/ci-cd.yml", "w") as f:
    f.write(content)
