#!/bin/bash
# =============================================================================
# Google Cloud SDK (gcloud) Installer for GenX FX
# =============================================================================
# This script installs the Google Cloud CLI, also known as Google Shell,
# to enable management of GCP resources from your VPS or local machine.
# =============================================================================

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🤖 GenX FX: Installing Google Cloud SDK...${NC}"

# 1. Prerequisite check
if command -v gcloud &> /dev/null; then
    echo -e "${GREEN}✅ Google Cloud SDK is already installed.${NC}"
    gcloud version
else
    # 2. Add repo and install (Ubuntu/Debian)
    echo "📦 Adding Google Cloud repository..."
    sudo apt-get update
    sudo apt-get install -y apt-transport-https ca-certificates gnupg curl
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    sudo apt-get update && sudo apt-get install -y google-cloud-cli

    # 3. Finalize
    echo -e "${GREEN}✅ Google Cloud SDK installed successfully!${NC}"
fi

echo ""
echo "Next steps for GenX FX:"
echo "1. Authenticate: gcloud auth login"
echo "2. Set Project: gcloud config set project [YOUR_PROJECT_ID]"
echo "3. Run GCP Deployment: See docs/GCP_EXNESS_DEPLOYMENT.md"
