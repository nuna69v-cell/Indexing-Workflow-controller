#!/bin/bash
# Start ttyd (GUI terminal) in the background on port 7681
# It shares the bash shell over the web
echo "🚀 Starting GUI Terminal (ttyd) on port 7681..."
ttyd -p 7681 bash > ttyd.log 2>&1 &
echo "✅ GUI Terminal started. Access it at http://localhost:7681"
