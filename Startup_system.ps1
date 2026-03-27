# System Startup Script for Jule Development Environment
# Downloads and installs the latest Jule Compiler (julec) on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Jule Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"
$juleDir = "C:\jule"
$juleBinDir = Join-Path $juleDir "bin"

# 1. Check if already installed
if (Test-Path "$juleDir\julec.exe") {
    Write-Host "✓ Jule compiler is already installed at $juleDir" -ForegroundColor Green
} else {
    Write-Host "[1/3] Downloading latest Jule release..." -ForegroundColor Yellow

    # Create directory
    if (-not (Test-Path $juleDir)) {
        New-Item -ItemType Directory -Path $juleDir -Force | Out-Null
    }

    # Fetch latest release info from GitHub API
    try {
        $releaseUrl = "https://api.github.com/repos/julelang/jule/releases/latest"
        $releaseInfo = Invoke-RestMethod -Uri $releaseUrl -UseBasicParsing

        # Find Windows x64 asset
        $asset = $releaseInfo.assets | Where-Object { $_.name -match "windows-amd64" }

        if ($null -eq $asset) {
            Write-Host "✗ Could not find Windows amd64 release asset." -ForegroundColor Red
            return
        }

        $downloadUrl = $asset.browser_download_url
        $zipPath = Join-Path $env:TEMP "jule_latest.zip"

        Write-Host "  Downloading from $downloadUrl..." -ForegroundColor Gray
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath -UseBasicParsing

        Write-Host "[2/3] Extracting Jule..." -ForegroundColor Yellow
        Expand-Archive -Path $zipPath -DestinationPath $juleDir -Force

        # Cleanup
        Remove-Item $zipPath -Force

        # Jule releases usually extract to a versioned subfolder. We want to move contents up.
        # Check if there is exactly ONE item in the folder and if it is a directory.
        $contents = Get-ChildItem -Path $juleDir
        if ($contents.Count -eq 1 -and $contents[0].PSIsContainer) {
            $extractedFolder = $contents[0]
            Copy-Item -Path "$($extractedFolder.FullName)\*" -Destination $juleDir -Recurse -Force
            Remove-Item -Path $extractedFolder.FullName -Recurse -Force
        }

        Write-Host "✓ Extracted to $juleDir" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to download or extract Jule: $($_.Exception.Message)" -ForegroundColor Red
        return
    }
}

# 2. Add to PATH
Write-Host ""
Write-Host "[3/3] Configuring Environment Variables..." -ForegroundColor Yellow

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")

if (($userPath -notmatch [regex]::Escape($juleDir)) -and ($machinePath -notmatch [regex]::Escape($juleDir))) {
    Write-Host "  Adding $juleDir to User PATH..." -ForegroundColor Gray
    $newPath = $userPath + ";" + $juleDir
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")

    # Also update current session
    $env:Path = $env:Path + ";" + $juleDir
    Write-Host "✓ Added to PATH" -ForegroundColor Green
} else {
    Write-Host "✓ Jule directory is already in PATH" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Jule Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Please restart your terminal or run 'julec version' to verify." -ForegroundColor Cyan
