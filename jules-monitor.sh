#!/bin/bash
# GenX VisionOps - Continuous Monitoring Script (by Jules AI)
# This script monitors the GenX VisionOps infrastructure and restarts services if needed.

echo "===================================================="
echo "   GENX VISIONOPS - CONTINUOUS MONITORING (JULES)   "
echo "===================================================="

# 1. Check for PM2
if ! command -v pm2 &> /dev/null; then
    echo "[ERROR] PM2 not found. Please run ./jules-deploy.sh first."
    exit 1
fi

# 2. Monitor Services
echo "Monitoring GenX VisionOps services..."
pm2 monit
