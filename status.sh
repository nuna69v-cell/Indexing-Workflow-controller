#!/bin/bash
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
