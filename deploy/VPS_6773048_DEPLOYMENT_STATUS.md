# VPS Deployment Status (ID: 6773048)

**Deployment Date:** 2026-01-22
**Location:** Singapore (implied from context)
**Certificate CN:** secops.group

## Network Configuration

- **SSID:** LengA6-9V
- **Protocol:** Wi-Fi 4 (802.11n)
- **Security Type:** WPA2-Personal
- **Manufacturer:** Realtek Semiconductor Corp.
- **Description:** Realtek RTL8188EU Wireless LAN 802.11n USB 2.0 Network Adapter
- **Driver Version:** 1030.52.1216.2025
- **Network Band:** 2.4 GHz (Channel 1)
- **Link Speed (Rx/Tx):** 150/150 Mbps
- **Aggregated Link Speed (Receive/Transmit):** 150/150 Mbps
- **MAC Address:** 78:20:51:54:60:5C

### IP Configuration
- **IPv4 Address:** 192.168.18.6
- **IPv4 Gateway:** 192.168.18.1
- **IPv4 DNS:** 8.8.8.8 (Unencrypted), 1.1.1.1 (Unencrypted)
- **IPv6 Link-Local:** fe80::417b:4f29:7fd:caaa%12
- **IPv6 DNS:** 2001:4860:4860::8888 (Unencrypted), 2606:4700:4700::1111 (Unencrypted)

## SSL Certificate Details

- **Common Name (CN):** secops.group
- **Issuer:** R13 (Let's Encrypt)
- **Issued On:** Monday, November 17, 2025
- **Expires On:** Sunday, February 15, 2026
- **Certificate Hash:** 29997c96881c955e8add95f72d77d1c1a9793e5578ba6ae3c9cba36273bbe5c5
- **Public Key:** 8de36fb26d8ccc049760f41343611668e0bac3a0503a8f483f6eeb4e2d29807b

## Additional Context
- **Platform:** MQL5 / Windows (via Docker `dockur/windows` context)
- **Original Path:** `C:\Users\USER\AppData\Roaming\MetaQuotes\Terminal\53785E099C927DB68A545C249CDBCE06\MQL5\Shared Projects\EXNESS_GenX_Trading\DEPLOY\VPS_6773048_DEPLOYMENT_STATUS.md`

## Deployment Telemetry & Metrics
- **EA Initialized:** EXNESS GenX Trader v2.0
- **Configuration:** EURUSD, Strategy MA(10/30) + RSI(14), Risk: 1.0% per trade, Trading: ENABLED
- **Resource Usage:** 5 charts, 5 EAs, 0 custom indicators
- **Memory/CPU:** 4330 Mb RAM reserved, EA 0.00% CPU in 5 threads

## Security & Incidents
### Telegram Incomplete Login Incident (2026-01-21)
- **Time:** 2026-01-21 13:26:57 UTC
- **Device:** Telegram Android X, 0.28.3.1785-arm64-v8a, Samsung Galaxy A51, Android, 13 (33)
- **Location:** Phnom Penh, Cambodia
- **Status:** Incomplete login. The code was entered correctly, but no correct password was given. Nobody gained access to chats.
- **Action Required:**
  1. Terminate the incomplete login in Settings > Devices (or Privacy & Security > Active Sessions).
  2. Rotate `TELEGRAM_BOT_TOKEN` and any exposed system passwords.
  3. Ensure 2FA remains active on the Telegram account.

### SSL Certificate Renewal Action
- **CN:** secops.group
- **Expires On:** Sunday, February 15, 2026
- **Action Required:** Schedule certbot renewal before expiry to maintain secure `https://` WebRequest connections from MT5.
