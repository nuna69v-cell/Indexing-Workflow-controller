# GenX VisionOps Setup Script (PowerShell)
# This script installs dependencies and prepares the environment

Write-Host "Setting up GenX VisionOps Infrastructure..." -ForegroundColor Cyan

# 1. Install Node.js dependencies
if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "[1/3] Installing Node.js dependencies..." -ForegroundColor Green
    npm install
} else {
    Write-Host "[ERROR] npm not found. Please install Node.js." -ForegroundColor Red
    exit 1
}

# 2. Install Python dependencies
if (Get-Command pip -ErrorAction SilentlyContinue) {
    Write-Host "[2/3] Installing Python dependencies..." -ForegroundColor Green
    pip install -r requirements.txt || Write-Host "[WARNING] requirements.txt not found. Skipping pip install." -ForegroundColor Yellow
} elseif (Get-Command pip3 -ErrorAction SilentlyContinue) {
    Write-Host "[2/3] Installing Python 3 dependencies..." -ForegroundColor Green
    pip3 install -r requirements.txt || Write-Host "[WARNING] requirements.txt not found. Skipping pip3 install." -ForegroundColor Yellow
} else {
    Write-Host "[WARNING] pip not found. Skipping Python dependencies installation." -ForegroundColor Yellow
}

# 3. Prepare Data Directories
Write-Host "[3/3] Preparing data directories..." -ForegroundColor Green
New-Item -ItemType Directory -Path "data/logs" -Force | Out-Null
New-Item -ItemType Directory -Path "data/history" -Force | Out-Null
New-Item -ItemType Directory -Path "data/cache" -Force | Out-Null

Write-Host "Setup Complete. Run .\start.ps1 to begin." -ForegroundColor Cyan
