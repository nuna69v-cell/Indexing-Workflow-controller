#!/usr/bin/env python3
"""
Simple GenX FX Trading Startup Script for Container Environment
"""
import os
import subprocess
import sys
import time
from pathlib import Path

def setup_directories():
    print("🚀 Starting GenX FX Trading System...")
    Path("logs").mkdir(exist_ok=True)
    Path("backups").mkdir(exist_ok=True)

def start_web_server():
    print("🌐 Starting web server for signal distribution...")
    try:
        with open("logs/web_server.log", "w") as f:
            process = subprocess.Popen(
                ["python3", "-m", "http.server", "8080", "--directory", "signal_output"],
                stdout=f, stderr=subprocess.STDOUT
            )

        with open("logs/web_server.pid", "w") as f:
            f.write(str(process.pid))

        print(f"Web server started (PID: {process.pid})")
        return process.pid
    except Exception as e:
        print(f"Failed to start web server: {e}")
        return None

def create_signal_loop_script():
    script_content = """#!/bin/bash
source genx_env/bin/activate 2>/dev/null || true
while true; do
    echo "$(date): Generating signals..." >> logs/signals.log
    python3 demo_excel_generator.py >> logs/signals.log 2>&1

    # Try to run AMP if available
    python3 amp_cli.py run --once >> logs/amp.log 2>&1 || echo "$(date): AMP run failed" >> logs/amp.log

    # Wait 5 minutes
    sleep 300
done
"""
    with open("signal_loop.sh", "w") as f:
        f.write(script_content)
    os.chmod("signal_loop.sh", 0o755)

def start_signal_loop():
    print("📊 Starting automatic signal generation...")
    create_signal_loop_script()

    try:
        with open("logs/signal_loop.log", "w") as f:
            process = subprocess.Popen(
                ["nohup", "./signal_loop.sh"],
                stdout=f, stderr=subprocess.STDOUT,
                preexec_fn=os.setpgrp  # detach from parent
            )

        with open("logs/signal_loop.pid", "w") as f:
            f.write(str(process.pid))

        print(f"Signal generation started (PID: {process.pid})")
        return process.pid
    except Exception as e:
        print(f"Failed to start signal loop: {e}")
        return None

def create_status_script():
    script_content = """#!/bin/bash
echo "=== GenX FX Trading System Status ==="
echo "Date: $(date)"
echo

# Check if processes are running
WEB_PID=$(cat logs/web_server.pid 2>/dev/null)
SIGNAL_PID=$(cat logs/signal_loop.pid 2>/dev/null)

echo "🌐 Web Server:"
if kill -0 $WEB_PID 2>/dev/null; then
    echo "  ✅ Running (PID: $WEB_PID)"
    echo "  📡 URL: http://localhost:8080"
else
    echo "  ❌ Not running"
fi

echo "📊 Signal Generation:"
if kill -0 $SIGNAL_PID 2>/dev/null; then
    echo "  ✅ Running (PID: $SIGNAL_PID)"
else
    echo "  ❌ Not running"
fi

echo
echo "📁 Latest Signal Files:"
ls -la signal_output/ 2>/dev/null | tail -5

echo
echo "📈 Recent Activity:"
echo "Signal generation:"
tail -3 logs/signals.log 2>/dev/null || echo "  No logs yet"

echo
echo "💾 System Resources:"
df -h . | grep -v Filesystem
free -h | grep -v "Swap:"
"""
    with open("status.sh", "w") as f:
        f.write(script_content)
    os.chmod("status.sh", 0o755)

def create_stop_script():
    script_content = """#!/bin/bash
echo "🛑 Stopping GenX FX Trading System..."

# Read PIDs
WEB_PID=$(cat logs/web_server.pid 2>/dev/null)
SIGNAL_PID=$(cat logs/signal_loop.pid 2>/dev/null)

# Kill processes
if [ ! -z "$WEB_PID" ] && kill -0 $WEB_PID 2>/dev/null; then
    kill $WEB_PID
    echo "Web server stopped"
fi

if [ ! -z "$SIGNAL_PID" ] && kill -0 $SIGNAL_PID 2>/dev/null; then
    # Kill the process group to ensure child sleeps/pythons are also killed
    kill -- -$SIGNAL_PID 2>/dev/null || kill $SIGNAL_PID
    echo "Signal generation stopped"
fi

# Clean up PID files
rm -f logs/web_server.pid logs/signal_loop.pid

echo "✅ Trading system stopped"
"""
    with open("stop_trading.sh", "w") as f:
        f.write(script_content)
    os.chmod("stop_trading.sh", 0o755)

def generate_initial_signals():
    print("📊 Generating initial signals...")
    subprocess.run(["python3", "demo_excel_generator.py"], check=False)

def print_summary():
    print("✅ GenX FX Trading System is now running!")
    print()
    print("📋 Management Commands:")
    print("  📊 Check Status:    ./status.sh")
    print("  🛑 Stop System:     ./stop_trading.sh")
    print("  🔄 Restart:         ./stop_trading.sh && python3 start_trading.py")
    print()
    print("📡 Access Points:")
    print("  🌐 Web Interface:   http://localhost:8080")
    print("  📈 MT4 Signals:     http://localhost:8080/MT4_Signals.csv")
    print("  📈 MT5 Signals:     http://localhost:8080/MT5_Signals.csv")
    print("  📊 Excel File:      http://localhost:8080/genx_signals.xlsx")
    print()
    print("📝 Log Files:")
    print("  📊 Signals:         tail -f logs/signals.log")
    print("  🌐 Web Server:      tail -f logs/web_server.log")
    print("  🔄 AMP:             tail -f logs/amp.log")
    print()
    print("🎉 Your trading system is generating signals every 5 minutes!")

def main():
    setup_directories()
    start_web_server()
    start_signal_loop()
    create_status_script()
    create_stop_script()
    generate_initial_signals()
    print_summary()

if __name__ == "__main__":
    main()
