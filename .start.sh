#!/bin/bash
# GenX VisionOps - Automated Environment Initialization (.start.sh)
# This script automates the "Getting Started" steps for the GenX VisionOps infrastructure.

echo "===================================================="
echo "   GENX VISIONOPS - INFRASTRUCTURE INITIALIZER      "
echo "===================================================="

# 1. Authenticate with Google Cloud
echo "[1/5] Authenticating with Google Cloud..."
gcloud auth application-default login --no-launch-browser

# 2. Initialize Terraform
echo "[2/5] Initializing Terraform Infrastructure..."
if [ -d "terraform" ]; then
    cd terraform
    terraform init
    terraform apply -auto-approve
    cd ..
else
    echo "[ERROR] Terraform directory not found."
fi

# 3. Start Cloud Workstation
echo "[3/5] Starting Cloud Workstation (trading-ide)..."
gcloud workstations start trading-ide \
    --cluster=trading-cluster \
    --config=trading-ide-config \
    --region=us-central1

# 4. Clone MQL5 Trading Robots (NUNA)
echo "[4/6] Cloning MQL5 Trading Robots (NUNA)..."
if [ ! -d "NUNA" ]; then
    git clone https://github.com/A6-9V/NUNA.git
else
    echo "NUNA repository already exists. Pulling latest changes..."
    cd NUNA && git pull && cd ..
fi

# 5. Install Windows Compatibility Layer (Wine)
echo "[5/6] Checking for Windows Compatibility (Wine)..."
if ! command -v wine &> /dev/null; then
    echo "Installing Wine 9.0+..."
    sudo dpkg --add-architecture i386
    sudo apt update
    sudo apt install -y wine64 wine32
else
    echo "Wine is already installed."
fi

# 6. Launch Central Brain
echo "[6/6] Launching Central Brain (Node.js)..."
npm run dev

echo "===================================================="
echo "   SYSTEM INITIALIZATION COMPLETE                   "
echo "===================================================="
