# 🚀 GenX FX AWS Free Tier Deployment Guide

Deploy your GenX FX trading system to AWS using the **free tier** - perfect for getting started without any costs!

## 🎯 What You'll Get

- **EC2 t2.micro instance** (750 hours/month FREE)
- **Public IP address** for web access
- **CloudWatch monitoring** (5GB logs/month FREE)
- **15GB data transfer/month** (FREE)
- **Estimated cost after free tier**: $5-15/month

---

## 📋 Prerequisites

### 1. AWS Account Setup
```bash
# Create AWS account at https://aws.amazon.com/free/
# Enable billing alerts in AWS Console
```

### 2. Install AWS CLI
```bash
# Windows (PowerShell)
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# macOS
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### 3. Configure AWS Credentials
```bash
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key  
# - Default region: us-east-1
# - Default output format: json
```

---

## 🚀 Quick Deployment (5 Minutes)

### Option 1: One-Command Deployment
```bash
# Clone repository (replace YourUsername with your actual GitHub username!)
git clone https://github.com/YourUsername/GenX_FX.git
cd GenX_FX

# Make script executable
chmod +x deploy/free-tier-deploy.sh

# Deploy with auto-generated key pair
./deploy/free-tier-deploy.sh --key-pair genx-fx-key
```

### Option 2: Step-by-Step Deployment
```bash
# 1. Create EC2 key pair
aws ec2 create-key-pair --key-name genx-fx-key --region us-east-1 --query 'KeyMaterial' --output text > genx-fx-key.pem
chmod 400 genx-fx-key.pem

# 2. Deploy CloudFormation stack
aws cloudformation deploy \
  --template-file deploy/aws-free-tier-deploy.yml \
  --stack-name production-genx-fx-free-tier \
  --parameter-overrides Environment=production KeyPairName=genx-fx-key \
  --capabilities CAPABILITY_IAM \
  --region us-east-1

# 3. Get deployment info
aws cloudformation describe-stacks \
  --stack-name production-genx-fx-free-tier \
  --region us-east-1 \
  --query 'Stacks[0].Outputs'
```

---

## 📊 Deployment Output

After successful deployment, you'll see:

```bash
=== GenX FX Deployment Information ===
Instance IP: 54.123.456.789
Application URL: http://54.123.456.789:8000
SSH Command: ssh -i genx-fx-key.pem ec2-user@54.123.456.789

=== Next Steps ===
1. Wait 5-10 minutes for the application to start
2. Access your trading platform at: http://54.123.456.789:8000
3. SSH into the server: ssh -i genx-fx-key.pem ec2-user@54.123.456.789
4. Check logs: docker logs genx-fx
```

---

## 🔧 Post-Deployment Setup

### 1. Access Your Trading Platform
```bash
# Open in browser
http://YOUR_INSTANCE_IP:8000

# Check API health
curl http://YOUR_INSTANCE_IP:8000/health
```

### 2. SSH into Your Server
```bash
ssh -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP

# Check application status
docker ps
docker logs genx-fx

# View real-time logs
docker logs -f genx-fx
```

### 3. Configure Trading Settings
```bash
# SSH into server
ssh -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP

# Edit environment variables
cd GenX_FX
nano .env

# Restart application
docker restart genx-fx
```

---

## 📈 Monitoring & Management

### 1. CloudWatch Monitoring
```bash
# View CPU usage
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=YOUR_INSTANCE_ID \
  --statistics Average \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z \
  --period 3600

# View application logs
aws logs describe-log-streams --log-group-name /aws/ec2/production-genx-fx
```

### 2. Application Management
```bash
# SSH into server
ssh -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP

# Restart application
docker restart genx-fx

# Update application
cd GenX_FX
git pull origin main
docker build -f Dockerfile.free-tier -t genx-fx .
docker stop genx-fx
docker rm genx-fx
docker run -d -p 8000:8000 --name genx-fx --restart unless-stopped genx-fx

# View trading signals
curl http://localhost:8000/MT4_Signals.csv
```

### 3. Backup Your Data
```bash
# Run the auto-generated backup script
./backup-genx.sh

# Manual backup
docker exec genx-fx tar czf - /app/data /app/logs > genx-backup-$(date +%Y%m%d).tar.gz
```

---

## 💰 Cost Management

### Free Tier Limits (12 months)
- ✅ **EC2 t2.micro**: 750 hours/month
- ✅ **EBS Storage**: 30GB/month
- ✅ **Data Transfer**: 15GB/month
- ✅ **CloudWatch**: 5GB logs/month

### Cost After Free Tier
- **EC2 t2.micro**: ~$8.50/month
- **EBS Storage (20GB)**: ~$2/month
- **Data Transfer**: ~$1-3/month
- **Total**: ~$12-15/month

### Cost Optimization Tips
```bash
# 1. Stop instance when not trading
aws ec2 stop-instances --instance-ids YOUR_INSTANCE_ID

# 2. Start instance when needed
aws ec2 start-instances --instance-ids YOUR_INSTANCE_ID

# 3. Set up billing alerts
aws budgets create-budget --account-id YOUR_ACCOUNT_ID --budget file://budget.json

# 4. Monitor usage
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-01-31 --granularity MONTHLY --metrics BlendedCost
```

---

## 🔒 Security Best Practices

### 1. Secure SSH Access
```bash
# Restrict SSH to your IP only
aws ec2 authorize-security-group-ingress \
  --group-id YOUR_SECURITY_GROUP_ID \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP_ADDRESS/32
```

### 2. Enable HTTPS (Optional)
```bash
# Install Let's Encrypt SSL certificate
ssh -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP

sudo yum install -y certbot
sudo certbot certonly --standalone -d your-domain.com

# Update Docker container to use SSL
docker run -d -p 443:8000 -v /etc/letsencrypt:/etc/letsencrypt --name genx-fx-ssl genx-fx
```

### 3. Regular Updates
```bash
# SSH into server
ssh -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP

# Update system
sudo yum update -y

# Update application
cd GenX_FX
git pull origin main
docker build -f Dockerfile.free-tier -t genx-fx .
docker restart genx-fx
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. Application Not Starting
```bash
# Check Docker logs
docker logs genx-fx

# Check if port is open
netstat -tlnp | grep 8000

# Restart Docker service
sudo service docker restart
docker restart genx-fx
```

#### 2. Can't Access Web Interface
```bash
# Check security group rules
aws ec2 describe-security-groups --group-ids YOUR_SECURITY_GROUP_ID

# Test connectivity
curl -I http://YOUR_INSTANCE_IP:8000
```

#### 3. High CPU Usage
```bash
# Check resource usage
docker stats genx-fx

# Scale down if needed
docker update --cpus="0.5" --memory="512m" genx-fx
```

#### 4. Out of Disk Space
```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a

# Clean up logs
sudo find /var/log -name "*.log" -type f -mtime +7 -delete
```

---

## 📞 Support & Next Steps

### Getting Help
1. **Check logs**: `docker logs genx-fx`
2. **GitHub Issues**: Open an issue with error details
3. **AWS Support**: Use AWS free tier support for infrastructure issues

### Scaling Up
When you're ready to scale beyond free tier:

1. **Upgrade to t3.small** for better performance
2. **Add RDS database** for production data storage
3. **Use Application Load Balancer** for high availability
4. **Deploy to multiple regions** for global access

### Advanced Features
```bash
# Enable auto-scaling
aws autoscaling create-auto-scaling-group --auto-scaling-group-name genx-fx-asg

# Add CloudFront CDN
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json

# Set up Route 53 DNS
aws route53 create-hosted-zone --name your-domain.com
```

---

## 🎉 Success! Your GenX FX is Live!

🌐 **Access your trading platform**: `http://YOUR_INSTANCE_IP:8000`  
📊 **Download signals**: `http://YOUR_INSTANCE_IP:8000/MT4_Signals.csv`  
🔧 **SSH access**: `ssh -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP`  

**Happy Trading with GenX FX on AWS! 🚀**

---

## 🧹 Deleting the Stack (to avoid charges)

If you want to remove all AWS resources and avoid any charges, run:

```bash
aws cloudformation delete-stack --stack-name production-genx-fx-free-tier --region us-east-1
```

---

## ⚠️ IMPORTANT REMINDERS

- In your CloudFormation template, update the repository URL to your actual GitHub username.
- Always use Dockerfile.free-tier for AWS Free Tier deployments.
---

## 🛡️ Free VPN Setup (WireGuard)

Adding a VPN adds an extra layer of security, allowing you to access your trading platform as if you were on the same local network, without exposing it to the public internet. We recommend **WireGuard** as it is fast, modern, and lightweight—perfect for a free tier `t2.micro` instance.

### 1. Install WireGuard via PiVPN (Easiest Method)
PiVPN is a script that automates the installation and configuration of WireGuard.

\`\`\`shell
# SSH into your EC2 instance
ssh -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP

# Run the PiVPN installer
curl -L https://install.pivpn.io | bash
\`\`\`

**During the installation:**
*   **Network Interface:** Select `eth0`.
*   **Local IP:** Choose the static IP option (it uses the internal IP of the EC2 instance).
*   **Local Users:** Choose `ec2-user`.
*   **Installation Mode:** Select **WireGuard**.
*   **Port:** The default is `51820`. *Important: You must open this port in your AWS Security Group!*
*   **DNS Provider:** Choose a public DNS provider like `Quad9` or `Cloudflare` (1.1.1.1).
*   **Public IP or DNS:** Select your EC2 instance's Public IP address.
*   **Unattended Upgrades:** Enable them for security updates.
*   **Reboot:** Allow the system to reboot when finished.

### 2. Update AWS Security Group
You need to allow incoming UDP traffic on the WireGuard port.

\`\`\`shell
# Allow UDP traffic on port 51820 from anywhere
aws ec2 authorize-security-group-ingress \
  --group-id YOUR_SECURITY_GROUP_ID \
  --protocol udp \
  --port 51820 \
  --cidr 0.0.0.0/0
\`\`\`

### 3. Create a Client Configuration
After the EC2 instance reboots, reconnect and create a configuration for your personal device (laptop, phone, etc.).

\`\`\`shell
# Re-connect via SSH
ssh -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP

# Add a new client
pivpn add
# Enter a name for the client (e.g., 'mylaptop')

# The configuration file will be saved in /home/ec2-user/configs/mylaptop.conf
\`\`\`

### 4. Connect from Your Device
1.  Download the WireGuard client for your device (Windows, macOS, iOS, Android) from [wireguard.com](https://www.wireguard.com/install/).
2.  Transfer the \`mylaptop.conf\` file from your EC2 instance to your personal device.
    \`\`\`shell
    # Run this on your local machine (not the EC2 instance)
    scp -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP:/home/ec2-user/configs/mylaptop.conf ./
    \`\`\`
3.  Import the \`.conf\` file into the WireGuard application and click **Connect**.

*You are now connected to your AWS instance via VPN!*

---

## 🔒 Enhanced Security Practices

When exposing your trading platform, security is paramount. Since we are using an EC2 instance, you should implement these extra measures to prevent unauthorized access.

### 1. Configure AWS Security Groups (Network Level Firewall)
Ensure your Security Group ONLY allows traffic on necessary ports.

1.  Go to the **EC2 Dashboard** -> **Security Groups**.
2.  Select your Security Group (\`YOUR_SECURITY_GROUP_ID\`).
3.  Click **Edit inbound rules**.
4.  Configure the rules as follows:
    *   **SSH (Port 22):** Change "Source" from \`0.0.0.0/0\` to your specific IP address, OR restrict it to the VPN's IP range if you configured your VPN to allow internal network access.
    *   **HTTP (Port 80) / HTTPS (Port 443):** Allow \`0.0.0.0/0\` ONLY if you want the public internet to reach the web interface. *If you use a VPN, you can remove these public rules.*
    *   **Custom TCP (Port 8000):** This is the application port. Allow \`0.0.0.0/0\` only if the public needs access, otherwise restrict it.
    *   **Custom UDP (Port 51820):** Allow \`0.0.0.0/0\` (This is required for the VPN to connect).

### 2. Set Up UFW (Uncomplicated Firewall) on the Instance
While AWS Security Groups provide network-level protection, a local firewall provides defense-in-depth.

\`\`\`shell
# SSH into your EC2 instance
ssh -i genx-fx-key.pem ec2-user@YOUR_INSTANCE_IP

# Install UFW
sudo yum install ufw -y # Or apt-get install ufw on Ubuntu

# Allow necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 51820/udp # WireGuard VPN
sudo ufw allow 8000/tcp  # Application port

# Enable the firewall
sudo ufw enable
\`\`\`

### 3. Install Fail2ban to Prevent Brute Force Attacks
Fail2ban monitors logs (like SSH) and temporarily bans IP addresses that show malicious signs, such as too many password failures.

\`\`\`shell
# Install Fail2ban
sudo amazon-linux-extras install epel -y # For Amazon Linux 2
sudo yum install fail2ban -y

# Enable and start the service
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Verify it is running
sudo fail2ban-client status
\`\`\`

### 4. Keep the System Updated
Regularly update your system to patch vulnerabilities.

\`\`\`shell
# Update all packages
sudo yum update -y
\`\`\`
