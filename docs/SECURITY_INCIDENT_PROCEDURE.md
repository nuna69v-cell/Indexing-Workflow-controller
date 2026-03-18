# Security Incident Follow-up (Telegram Attempt, 2026-01-21)

## Details
An unauthorized login attempt was detected from Phnom Penh on Jan 21, 2026. The SMS code was correct, but the Two-Step Verification (2FA) password blocked the attacker.

## Checklist for Credentials Rotation
1. **Telegram:**
   - Active Sessions: Terminated any unrecognized devices.
   - Change 2FA password on Telegram.
   - If a `TELEGRAM_BOT_TOKEN` was used or stored on a compromised device/environment, rotate it via `@BotFather`.

2. **MT5 / VPS:**
   - The EA is running on the VPS associated with `VPS_6773048_DEPLOYMENT_STATUS.md`.
   - Update `EXNESS_GenX_Trader.mq5` to connect via HTTPS using the valid `secops.group` certificate to prevent MITM attacks on the local network (192.168.18.x).

3. **API Keys:**
   - Ensure the EA uses a dynamically generated or securely loaded `API_KEY` rather than a hardcoded blank or static key that can be extracted from the .ex5.
