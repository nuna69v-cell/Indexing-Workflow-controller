with open(".github/workflows/ci-cd.yml", "r") as f:
    content = f.read()

# Fix metadata multi-line
old_meta = """    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.DOCKER_REGISTRY }}/${{ github.repository_owner }}/${{ env.IMAGE_NAME }}
        tags: 'type=schedule

          type=ref,event=branch

          type=ref,event=pr

          type=semver,pattern={{version}}

          type=semver,pattern={{major}}.{{minor}}

          type=semver,pattern={{major}}

          type=sha,prefix={{branch}}-

          type=raw,value=latest,enable={{is_default_branch}}
          '"""

new_meta = """    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.DOCKER_REGISTRY }}/${{ github.repository_owner }}/${{ env.IMAGE_NAME }}
        tags: |
          type=schedule
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=semver,pattern={{major}}
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}"""

content = content.replace(old_meta, new_meta)

with open(".github/workflows/ci-cd.yml", "w") as f:
    f.write(content)
