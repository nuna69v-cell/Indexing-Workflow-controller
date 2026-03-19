#!/bin/bash
set -e

echo "🚀 Starting Jules Optimized Setup..."

# 1. Node.js Setup
echo "📦 Installing Node.js dependencies..."
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

# 5. GUI Terminal Setup
echo "🖥️  Starting GUI Terminal..."
if [ -x "./start_gui_terminal.sh" ]; then
    ./start_gui_terminal.sh || echo "⚠️ Failed to start GUI Terminal"
else
    echo "⚠️ start_gui_terminal.sh not found or not executable"
fi

echo "✅ Setup Complete! Environment is ready for snapshot."
