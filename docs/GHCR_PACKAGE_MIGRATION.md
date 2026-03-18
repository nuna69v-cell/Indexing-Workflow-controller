# GHCR Package Discrepancy

**Observation (from User Upload 20260318_165427.jpg):**
The GitHub Container Registry page shows the `ghcr.io/Mouy-leng/genx:main` image was last published 6 months ago.

**Analysis of Repository:**
The `.github/workflows/ci-cd.yml` file is configured with:
```yaml
env:
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: genx-fx
```

This points to `ghcr.io/Mouy-leng/genx-fx`, rather than `ghcr.io/Mouy-leng/genx`.

**Action Needed:**
To consolidate or fix this so the community/servers pull the active image:
1. Update any deployment scripts (e.g., in the `deploy/` directory) that might still reference the outdated `genx` container.
2. If `genx` is the desired package name instead of `genx-fx`, the CI/CD pipeline `IMAGE_NAME` needs to be updated.

**Update (2026-03-18):**
Modified `.github/workflows/ci-cd.yml` to set `IMAGE_NAME: genx` to match the package from the screenshot `ghcr.io/Mouy-leng/genx:main`, which had not been updated in 6 months. This will cause the next CI run to publish to the correct repository container registry package.
