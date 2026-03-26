# GenX VisionOps Start Script (PowerShell)
# This script starts the Central Brain (Node.js) and the Autonomous AI Orchestrator (Python)

Write-Host "Starting GenX VisionOps Infrastructure..." -ForegroundColor Cyan

# 1. Check for Node.js
if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host "[1/3] Starting Central Brain (Node.js)..." -ForegroundColor Green
    Start-Process -NoNewWindow -FilePath "npm" -ArgumentList "run dev"
} else {
    Write-Host "[ERROR] Node.js not found. Please install Node.js." -ForegroundColor Red
    exit 1
}

# 2. Check for Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "[2/3] Starting Autonomous AI Orchestrator (Python)..." -ForegroundColor Green
    Start-Process -NoNewWindow -FilePath "python" -ArgumentList "main.py"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    Write-Host "[2/3] Starting Autonomous AI Orchestrator (Python 3)..." -ForegroundColor Green
    Start-Process -NoNewWindow -FilePath "python3" -ArgumentList "main.py"
} else {
    Write-Host "[ERROR] Python not found. Please install Python." -ForegroundColor Red
    exit 1
}

Write-Host "[3/3] System Online. Access Dashboard at http://localhost:3000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop all processes (Note: You may need to kill them manually if they run in background)." -ForegroundColor Yellow

# Keep the script running to monitor logs if needed, or just exit
# while($true) { Start-Sleep -Seconds 1 }
