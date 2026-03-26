# GenX VisionOps - VPS Deployment Guide

This guide will help you deploy the GenX VisionOps infrastructure to a Virtual Private Server (VPS) like **Google Compute Engine**, **AWS EC2**, or **DigitalOcean**.

## 1. Prepare your VPS
Provision a Linux VM (Ubuntu 22.04 LTS or Debian 11+ recommended) with at least:
- 2 vCPUs
- 4GB RAM
- 20GB Disk

## 2. Initial Server Setup
Connect to your VPS via SSH and run these commands to install the necessary runtimes:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js (v20+)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python 3 and pip
sudo apt install -y python3 python3-pip python3-venv

# Install PM2 globally for process management
sudo npm install -g pm2
```

## 3. Clone and Initialize
Clone your repository (or upload the files) to the server:

```bash
# Navigate to your app directory
cd /path/to/genx-visionops

# Install dependencies
npm install
pip3 install -r requirements.txt

# Ensure scripts are executable
chmod +x setup.sh start.sh jules-deploy.sh
```

## 4. Configuration
Ensure your `firebase-applet-config.json` is present in the root directory. This file is critical for connecting to your Firestore database.

## 5. Deployment with PM2 (Recommended)
Use the Jules AI deployment script to start the Central Brain and AI Orchestrator in the background:

```bash
# Start the deployment
./jules-deploy.sh
```

### Useful PM2 Commands:
- `pm2 status`: Check if processes are running.
- `pm2 logs`: View real-time logs for both Node.js and Python.
- `pm2 monit`: Open a visual monitoring dashboard in your terminal.
- `pm2 restart all`: Restart the entire infrastructure.

## 6. Firewall Configuration
Ensure port **3000** (or your custom `PORT`) is open in your VPS firewall settings to allow access to the dashboard.

## 7. Persistence
To ensure GenX VisionOps starts automatically if the server reboots:

```bash
pm2 startup
# (Follow the instructions provided by the command above)
pm2 save
```

---
*GenX VisionOps - Autonomous AI Trading Infrastructure*
