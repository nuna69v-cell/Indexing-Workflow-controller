#!/bin/bash
echo "Cleaning up ghost files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name ".DS_Store" -delete 2>/dev/null
find . -type f -name "npm-debug.log*" -delete 2>/dev/null
find . -type f -name "yarn-error.log*" -delete 2>/dev/null
echo "Cleaning up dangling Docker resources..."
docker system prune -f 2>/dev/null || true
echo "Cleanup complete."
