# SSH Setup for Project

This project has been configured to use SSH for all existing connections.

## SSH Key Details

- **Type**: Ed25519
- **Path**: `~/.ssh/id_ed25519`
- **Public Key**:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEeSLWKibLOYIOA794iClIT7WU/32N1BbfzHR8hopSGG jules@google.com
```

## Configured Connections

### 1. GitHub
The git remote `origin` has been updated to use SSH:
`git@github.com:A6-9V/MQL5-Google-Onedrive.git`

**Action Required**:
Please add the public key above to your GitHub account:
[GitHub SSH Key Settings](https://github.com/settings/keys)

### 2. MQL5 Forge (Manual Setup)
If you wish to use SSH with Forge, add the public key to your Forge profile:
[Forge SSH Key Settings](https://forge.mql5.io/user/settings/ssh)

Then update the remote (if you add one):
`git remote add forge git@forge.mql5.io:LengKundee/mql5.git`

### 3. VPS (Manual Setup)
To enable SSH access to your VPS without a password:
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-vps-ip
```
Or manually append the public key to `~/.ssh/authorized_keys` on the VPS.

## Verifying Setup
Once the key is added to GitHub, you can test the connection:
```bash
ssh -T git@github.com
```

## SSH Key Management

### Checking Existing SSH Keys
To see all SSH keys configured in this repository and associated services:

1. **Local SSH Keys**:
   ```bash
   ls -la ~/.ssh/
   ```

2. **GitHub Personal Keys**:
   - Visit: https://github.com/settings/keys
   - Lists all SSH keys for your account

3. **GitHub Deploy Keys** (Repository-specific):
   - Visit: https://github.com/A6-9V/MQL5-Google-Onedrive/settings/keys
   - Lists keys with read/write access to this repository only

4. **GitHub Actions Secrets**:
   - Visit: https://github.com/A6-9V/MQL5-Google-Onedrive/settings/secrets/actions
   - May contain SSH private keys stored as secrets

### SSH Key Audit
For a detailed audit of SSH keys associated with this repository, see:
- [SSH Key Audit Report](docs/SSH_KEY_AUDIT.md)

### Best Practices
- Use **Ed25519** keys (more secure than RSA or ECDSA)
- Rotate keys every 6-12 months
- Use separate keys for different purposes (deploy vs. personal)
- Remove unused or unknown keys
- Never commit private keys to the repository
