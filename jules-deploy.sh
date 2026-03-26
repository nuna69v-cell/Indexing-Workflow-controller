#!/bin/bash
# GenX VisionOps - Continuous Deployment Script (by Jules AI)
# This script ensures the GenX VisionOps infrastructure runs continuously in the cloud.

echo "===================================================="
echo "   GENX VISIONOPS - CONTINUOUS DEPLOYMENT (JULES)   "
echo "===================================================="

# 1. Check for PM2
if ! command -v pm2 &> /dev/null; then
    echo "[1/4] PM2 not found. Installing PM2 globally..."
    npm install -g pm2
else
    echo "[1/4] PM2 is already installed."
fi

# 2. Run Setup
echo "[2/4] Running Environment Setup..."
./setup.sh

# 3. Start Continuous Monitoring
echo "[3/4] Starting GenX VisionOps via PM2..."
pm2 start pm2.config.cjs

# 4. Save PM2 Process List
echo "[4/4] Saving PM2 process list for persistence..."
pm2 save

echo "===================================================="
echo "   CONTINUOUS DEPLOYMENT ACTIVE                     "
echo "   Dashboard: http://localhost:3000                 "
echo "   Monitor:   pm2 monit                             "
echo "===================================================="
