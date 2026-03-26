#!/bin/bash
# GenX VisionOps Start Script (Linux/macOS)
# This script starts the Central Brain (Node.js) and the Autonomous AI Orchestrator (Python)

echo "Starting GenX VisionOps Infrastructure..."

# 1. Check for Node.js
if command -v node &> /dev/null; then
    echo "[1/3] Starting Central Brain (Node.js)..."
    npm run dev &
else
    echo "[ERROR] Node.js not found. Please install Node.js."
    exit 1
fi

# 2. Check for Python
if command -v python &> /dev/null; then
    echo "[2/3] Starting Autonomous AI Orchestrator (Python)..."
    python main.py &
elif command -v python3 &> /dev/null; then
    echo "[2/3] Starting Autonomous AI Orchestrator (Python 3)..."
    python3 main.py &
else
    echo "[ERROR] Python not found. Please install Python."
    exit 1
fi

echo "[3/3] System Online. Access Dashboard at http://localhost:3000"
echo "Press Ctrl+C to stop all processes (Note: You may need to kill them manually if they run in background)."

# Keep the script running to monitor logs if needed, or just exit
# while :; do sleep 1; done
wait
