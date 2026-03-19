<#
.SYNOPSIS
    Packages the GenX_FX Dev Environment into a zip archive for ASUS WebStorage backup.
.DESCRIPTION
    This script excludes heavy/dynamic dependencies (node_modules, venv, .git)
    that cause sync conflicts and high CPU usage in consumer cloud sync apps like ASUS WebStorage.
    It creates a clean archive suitable for safe cloud storage.
#>

param (
    [string]$DestinationPath = "$env:USERPROFILE\ASUS WebStorage\Backups\GenX_FX",
    [string]$SourcePath = ".\"
)

# Ensure destination exists
if (!(Test-Path -Path $DestinationPath)) {
    New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
    Write-Host "Created destination folder: $DestinationPath" -ForegroundColor Green
}

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ArchiveName = "GenX_FX_Backup_$Timestamp.zip"
$ArchiveFullPath = Join-Path -Path $DestinationPath -ChildPath $ArchiveName

Write-Host "Starting backup of GenX_FX environment..." -ForegroundColor Cyan

# Define exclusions (relative to SourcePath)
$Exclusions = @(
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "dist",
    "build",
    "expert-advisors\build",
    ".pytest_cache"
)

# Create a temporary directory to copy allowed files
$TempDir = Join-Path -Path [System.IO.Path]::GetTempPath() -ChildPath "GenX_FX_Temp_$Timestamp"
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

Write-Host "Copying files (excluding dependencies)..."
# Use robocopy for robust copying with exclusions
$RobocopyArgs = @(
    $SourcePath,
    $TempDir,
    "/E",           # Copy subdirectories, including empty ones
    "/XD"           # Exclude directories
) + $Exclusions + @(
    "/R:0",         # 0 retries on failed copies
    "/W:0",         # 0 wait time between retries
    "/NFL",         # No file list in output
    "/NDL",         # No directory list in output
    "/NJH",         # No job header
    "/NJS"          # No job summary
)

& robocopy @RobocopyArgs | Out-Null

Write-Host "Compressing to $ArchiveFullPath..."
Compress-Archive -Path "$TempDir\*" -DestinationPath $ArchiveFullPath -Force

Write-Host "Cleaning up temporary files..."
Remove-Item -Path $TempDir -Recurse -Force

Write-Host "Backup completed successfully!" -ForegroundColor Green
Write-Host "ASUS WebStorage will now sync the archive: $ArchiveFullPath" -ForegroundColor Yellow
