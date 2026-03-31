# ASUS WebStorage Development Container Guide

This guide outlines how to configure and use ASUS WebStorage as an online storage container for your coding and development environment.

## The Challenge with Sync Apps

Consumer-grade auto-backup apps like ASUS WebStorage are designed for documents and photos. When applied to active development folders, they can cause serious issues:
- **File Locking:** The sync agent might lock files while you are compiling or saving, crashing your tools.
- **High CPU Usage:** Massive folders like `node_modules` or `.venv` change constantly, triggering relentless sync operations.
- **Git Corruption:** Syncing `.git` internal state across devices can lead to catastrophic repository corruption.

## Our Solution: The Archive Method

To safely utilize ASUS WebStorage, we employ an automated archival process. Instead of syncing the live environment, we package the environment into a clean container (`.zip` or `.tar.gz`), excluding problematic dependency directories, and save the archive into the ASUS WebStorage backup folder.

### Step 1: Configure ASUS WebStorage App
1. Install and launch the ASUS WebStorage application on your device.
2. Configure your sync/backup directory.
   - On Windows, this is typically: `C:\Users\<YourName>\ASUS WebStorage\Backups`
   - On Linux, point it to your mounted WebStorage location or the Linux app directory.
3. Ensure the app is running and actively watching this folder.

### Step 2: Running the Backup
When you are ready to upload your current progress to your online container, run the provided scripts.

**For Windows (NUNA device):**
```powershell
.\asus-webstorage-backup.ps1
```
*Note: This script uses robust file copying (`robocopy`) and exclusions to create a safe `.zip` file, placed directly into your ASUS WebStorage Backup folder.*

**For Linux / WSL:**
```bash
./asus-webstorage-backup.sh
```
*Note: Creates a clean `.tar.gz` archive, ignoring dependencies.*

### Step 3: Restoring the Container
To restore your development environment on another device:
1. Allow ASUS WebStorage to sync the backup archive to your new device.
2. Extract the archive (`.zip` or `.tar.gz`) to your desired workspace folder.
3. Because heavy dependencies are excluded, you will need to re-initialize your local environment:
   - Run `npm install` or `pnpm install`
   - Set up your Python environment: `python3 -m venv .venv` and `pip install -r requirements.txt`
   - If `.git` was excluded (recommended), you can re-clone the repository and copy the extracted files over to keep your local uncommitted changes, or manage code through GitHub separately and use WebStorage purely for artifact backups.
