#!/bin/bash
# Packages the GenX_FX Dev Environment into a tar.gz archive for ASUS WebStorage backup.
# Excludes heavy/dynamic dependencies that cause sync conflicts.

set -e

SOURCE_DIR="."
# Default ASUS WebStorage path on Linux (adjust if mounted elsewhere)
DEST_DIR="$HOME/ASUS WebStorage/Backups/GenX_FX"

# Ensure destination exists
mkdir -p "$DEST_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="GenX_FX_Backup_$TIMESTAMP.tar.gz"
ARCHIVE_FULL_PATH="$DEST_DIR/$ARCHIVE_NAME"

echo "Starting backup of GenX_FX environment..."

# Compress excluding heavy directories
echo "Compressing to $ARCHIVE_FULL_PATH..."
tar -czvf "$ARCHIVE_FULL_PATH"     --exclude="node_modules"     --exclude=".venv"     --exclude="venv"     --exclude="__pycache__"     --exclude=".git"     --exclude="dist"     --exclude="build"     --exclude="expert-advisors/build"     --exclude=".pytest_cache"     -C "$SOURCE_DIR" . > /dev/null

echo "Backup completed successfully!"
echo "ASUS WebStorage will now sync the archive: $ARCHIVE_FULL_PATH"
