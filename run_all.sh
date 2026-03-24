#!/bin/bash
set -e

# Load python requirements
# pip install -r requirements-cloud.txt || true
pip install typer rich yaml || true

# Kill any existing node/python process on those ports
kill -9 $(lsof -t -i:8080) 2>/dev/null || true
kill -9 $(lsof -t -i:5173) 2>/dev/null || true
kill -9 $(lsof -t -i:8000) 2>/dev/null || true

echo "Starting FastApi Backend..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
disown $BACKEND_PID

echo $BACKEND_PID > logs/web_server.pid

echo "Starting Python Main Agent/Runner..."
python3 main.py live > logs/agent.log 2>&1 &
AGENT_PID=$!
disown $AGENT_PID

echo $AGENT_PID > logs/signal_loop.pid

echo "Starting Node JS Client App..."
npm run dev > logs/frontend.log 2>&1 &
FRONTEND_PID=$!
disown $FRONTEND_PID

echo "All services running in background."
echo "Backend PID: $BACKEND_PID"
echo "Agent PID: $AGENT_PID"
echo "Frontend PID: $FRONTEND_PID"

echo "Check logs via tail -f logs/*.log"
