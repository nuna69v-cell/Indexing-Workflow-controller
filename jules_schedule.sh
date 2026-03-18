#!/usr/bin/env bash

# Jules Auto Schedule Script
# Handles cleanup, user commands, and trading operations

# 1. User specified command
echo "Toots"

# 2. Cleanup operations
echo "Running cleanup..."
# Remove log files older than 7 days
find logs/ -type f -name "*.log" -mtime +7 -delete || true
# Remove temporary report files older than 7 days
find logs/ -type f -name "amp_job_report_*.json" -mtime +7 -delete || true

# 3. Go live - Start trading system operation
echo "Starting trading system operation (Go live)..."
# Start the monitor job in the background using the unified CLI
python3 genx_unified_cli.py execute-job monitor --background

echo "Jules schedule operations completed successfully."
