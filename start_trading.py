#!/usr/bin/env python3
"""
Simple GenX FX Trading Startup Script

This script sets up directories, starts the signal distribution server and the signal generation loop in the background.
"""

import os
import subprocess
import time
import sys

def setup_directories():
    print("🚀 Starting GenX FX Trading System...")
    os.makedirs("logs", exist_ok=True)
    os.makedirs("backups", exist_ok=True)
    os.makedirs("signal_output", exist_ok=True)

def start_web_server():
    print("🌐 Starting web server for signal distribution...")
    try:
        # Start web server in background
        with open("logs/web_server.log", "w") as log_file:
            process = subprocess.Popen(
                [sys.executable, "-m", "http.server", "8080", "--directory", "signal_output"],
                stdout=log_file,
                stderr=log_file,
                start_new_session=True # Detach from parent
            )
            with open("logs/web_server.pid", "w") as pid_file:
                pid_file.write(str(process.pid))
            print(f"Web server started (PID: {process.pid})")
    except Exception as e:
        print(f"Error starting web server: {e}")

def start_signal_generation():
    print("📊 Starting automatic signal generation...")
    try:
        signal_script_content = """#!/bin/bash
source genx_env/bin/activate
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
            f.write(signal_script_content)

        os.chmod("signal_loop.sh", 0o755)

        with open("logs/signal_loop.log", "w") as log_file:
            process = subprocess.Popen(
                ["./signal_loop.sh"],
                stdout=log_file,
                stderr=log_file,
                start_new_session=True # Detach from parent
            )

            with open("logs/signal_loop.pid", "w") as pid_file:
                pid_file.write(str(process.pid))
            print(f"Signal generation started (PID: {process.pid})")

    except Exception as e:
        print(f"Error starting signal generation: {e}")

if __name__ == "__main__":
    # In python we can activate virtual env by simply doing this if we want to run script inside it,
    # but since this script is executed with potentially right environment or the bash script inside does it:

    setup_directories()
    start_web_server()
    start_signal_generation()

    print("📊 Generating initial signals...")
    # This might fail if demo_excel_generator.py is not present, wrap in try/except
    try:
        subprocess.run([sys.executable, "demo_excel_generator.py"], check=False)
    except Exception as e:
        print(f"Note: Could not run initial signal generation: {e}")

    print("✅ GenX FX Trading System is now running!")
    print()
    print("📋 Management Commands:")
    print("  📊 Check Status:    ./status.sh")
    print("  🛑 Stop System:     ./stop_trading.sh")
    print("  🔄 Restart:         ./stop_trading.sh && ./start_trading.py")
    print()
    print("📡 Access Points:")
    print("  🌐 Web Interface:   http://34.71.143.222:8080")
    print("  📈 MT4 Signals:     http://34.71.143.222:8080/MT4_Signals.csv")
    print("  📈 MT5 Signals:     http://34.71.143.222:8080/MT5_Signals.csv")
    print("  📊 Excel File:      http://34.71.143.222:8080/genx_signals.xlsx")
    print()
    print("📝 Log Files:")
    print("  📊 Signals:         tail -f logs/signals.log")
    print("  🌐 Web Server:      tail -f logs/web_server.log")
    print("  🔄 AMP:             tail -f logs/amp.log")
    print()
    print("🎉 Your trading system is generating signals every 5 minutes!")
