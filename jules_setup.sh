#!/bin/bash
set -e

echo "🚀 Starting Jules Optimized Setup..."

# 1. Node.js Setup
echo "📦 Installing Node.js dependencies..."

# Install Cursor CLI (agent)
echo "Installing Cursor CLI..."
mkdir -p "$HOME/.cursor/agent"
curl -fsSL https://downloads.cursor.com/lab/2026.03.18-f6873f7/linux/x64/agent-cli-package.tar.gz | tar -xz -C "$HOME/.cursor/agent"
export PATH="$HOME/.cursor/agent:$PATH"
echo 'export PATH="$HOME/.cursor/agent:$PATH"' >> ~/.bashrc

if ! command -v pnpm &> /dev/null; then
    echo "Installing pnpm..."
    npm install -g pnpm
fi
pnpm install

# 2. Python Setup
echo "🐍 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 3. Run Linters
echo "🔍 Running Linters..."
# Frontend Lint
if [ -f "package.json" ]; then
    echo "Running ESLint..."
    pnpm run lint || echo "⚠️ ESLint finished with warnings/errors"
fi

# Backend Lint (Python)
echo "Running Ruff & Black..."
if command -v ruff &> /dev/null; then
    ruff check . || echo "⚠️ Ruff found issues"
else
    echo "Ruff not found, skipping."
fi

if command -v black &> /dev/null; then
    black --check . || echo "⚠️ Black found formatting issues"
else
    echo "Black not found, skipping."
fi

# 4. Run Tests
echo "🧪 Running Tests..."
# Backend Tests
if [ -f "run_tests.py" ]; then
    echo "Running Python Tests (run_tests.py)..."
    python3 run_tests.py || echo "⚠️ Python tests failed"
elif [ -d "tests" ]; then
    echo "Running Python Tests (pytest)..."
    pytest || echo "⚠️ Python tests failed"
fi

# Frontend Tests
if [ -f "package.json" ]; then
    echo "Running Frontend Tests..."
    # 'vitest run' performs a single run instead of watch mode
    pnpm exec vitest run || echo "⚠️ Frontend tests failed"
fi

echo "✅ Setup Complete! Environment is ready for snapshot."
