#!/bin/bash
# GenX VisionOps Season 2 - DigitalOcean Deployment Script

set -e

RED='[0;31m'
GREEN='[0;32m'
YELLOW='[1;33m'
BLUE='[0;34m'
NC='[0m' # No Color

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

DROPLET_NAME="genx-visionops-s2"
REGION="lon1"
SIZE="s-2vcpu-4gb"
IMAGE="ubuntu-22-04-x64"

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    print_error "doctl is not installed. Please install doctl first."
    exit 1
fi

print_status "Authenticating doctl (make sure DIGITALOCEAN_ACCESS_TOKEN is set if not already authenticated)..."
# doctl auth init (Assuming already authenticated or token provided in env)

# Get SSH keys
SSH_KEYS=$(doctl compute ssh-key list --format ID --no-header | tr "
" "," | sed "s/,$//")
if [ -z "$SSH_KEYS" ]; then
    print_error "No SSH keys found in DigitalOcean account. Please add an SSH key first."
    exit 1
fi

print_status "Creating DigitalOcean Droplet: $DROPLET_NAME..."
doctl compute droplet create $DROPLET_NAME   --image $IMAGE   --size $SIZE   --region $REGION   --ssh-keys $SSH_KEYS   --enable-monitoring   --wait

DROPLET_IP=$(doctl compute droplet get $DROPLET_NAME --format PublicIPv4 --no-header)
print_success "Droplet created successfully with IP: $DROPLET_IP"

print_status "Waiting for SSH to be ready on $DROPLET_IP..."
sleep 30

print_status "Deploying via SSH..."
ssh -o StrictHostKeyChecking=no root@$DROPLET_IP << 'SSH_EOF'
    apt-get update && apt-get upgrade -y
    apt-get install -y git curl build-essential software-properties-common ufw

    # Install Python and Node.js
    add-apt-repository -y ppa:deadsnakes/ppa
    apt-get update
    apt-get install -y python3.12 python3.12-venv python3.12-dev nodejs npm
    npm install -g pnpm

    # Clone repository
    git clone https://github.com/Mouy-leng/GenX-EA_Script.git /opt/genx-visionops
    cd /opt/genx-visionops

    # Run setup
    chmod +x deploy/setup-exness-vps.sh
    ./deploy/setup-exness-vps.sh

    echo "Deployment completed on remote host!"
SSH_EOF

print_success "GenX VisionOps Season 2 deployed successfully on DigitalOcean!"
