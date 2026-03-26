#!/bin/bash
# GenX VisionOps Setup Script (Linux/macOS)
# This script installs dependencies and prepares the environment

echo "Setting up GenX VisionOps Infrastructure..."

# 1. Install Node.js dependencies
if command -v npm &> /dev/null; then
    echo "[1/3] Installing Node.js dependencies..."
    npm install
else
    echo "[ERROR] npm not found. Please install Node.js."
    exit 1
fi

# 2. Install Python dependencies
if command -v pip &> /dev/null; then
    echo "[2/3] Installing Python dependencies..."
    pip install -r requirements.txt || echo "[WARNING] requirements.txt not found. Skipping pip install."
elif command -v pip3 &> /dev/null; then
    echo "[2/3] Installing Python 3 dependencies..."
    pip3 install -r requirements.txt || echo "[WARNING] requirements.txt not found. Skipping pip3 install."
else
    echo "[WARNING] pip not found. Skipping Python dependencies installation."
fi

# 3. Prepare Data Directories
echo "[3/3] Preparing data directories..."
mkdir -p data/logs
mkdir -p data/history
mkdir -p data/cache

echo "Setup Complete. Run ./start.sh to begin."
chmod +x ./start.sh 2>/dev/null || true
