#!/usr/bin/env bash

# Jules Ghost File & Workspace Cleanup Utility
# Designed to keep the JetBrains Intelligent Community workspace lightweight and prevent "ghost" files.

echo "🧹 Starting Workspace Ghost File Cleanup..."

# 1. Clean up Python cache files
echo "🗑️ Removing __pycache__ and .pyc files..."
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# 2. Clean up Node cache/logs (keeping node_modules if needed, but removing error logs)
echo "🗑️ Removing npm/pnpm error logs..."
find . -type f -name "npm-debug.log*" -delete 2>/dev/null
find . -type f -name "yarn-error.log*" -delete 2>/dev/null
find . -type f -name "pnpm-debug.log*" -delete 2>/dev/null

# 3. Clean up OS specific metadata
echo "🗑️ Removing OS metadata files (.DS_Store, Thumbs.db)..."
find . -type f -name ".DS_Store" -delete 2>/dev/null
find . -type f -name "Thumbs.db" -delete 2>/dev/null

# 4. Clean up empty directories that might cause confusion
echo "🗑️ Removing empty directories..."
find . -type d -empty -not -path "./.git/*" -delete 2>/dev/null

# 5. Clean up dangling Docker resources (images, volumes, networks)
# Check if docker is running and accessible
if command -v docker &> /dev/null && docker info &> /dev/null; then
    echo "🐳 Cleaning up dangling Docker resources..."
    docker system prune -f --volumes 2>/dev/null
else
    echo "⚠️ Docker is not running or accessible. Skipping Docker cleanup."
fi

echo "✅ Cleanup complete! The workspace is now lean and free of ghost files."
