# GenX_FX Trading System

Advanced AI-Powered Forex Signal Generator for MT4/5 Expert Advisors.

## 🚀 Overview
GenX_FX is a comprehensive, production-ready trading platform that combines a Python FastAPI backend for AI-powered predictions and market analysis with a Node.js Express server and React frontend for user interaction.

## ✨ Features
- **AI-Powered Predictions**: Leverages machine learning models for high-probability trading signals.
- **Hybrid Architecture**: Combines Python's data processing power with Node.js's scalability.
- **MT4/MT5 Integration**: Seamlessly connects with MetaTrader Expert Advisors via CSV and API.
- **Real-time Monitoring**: Integrated dashboard for tracking account performance and system health.
- **Robust Risk Management**: Automated position sizing and risk controls.

## 📂 Project Structure
- `api/`: Python FastAPI backend.
- `client/`: React + TypeScript frontend.
- `services/server/`: Node.js Express proxy and static file server.
- `core/`: Core trading logic and strategies.
- `expert-advisors/`: MetaTrader EA source files.
- `docs/`: Comprehensive documentation and deployment guides.

## 🛠️ Getting Started
For local development and setup, please refer to:
- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Comprehensive Documentation](docs/COMPREHENSIVE_DOCUMENTATION.md)

## 🚢 Deployment
GenX_FX is designed for easy deployment on modern cloud platforms:
- **Railway**: [Railway Deployment Guide](docs/RAILWAY_DEPLOYMENT.md) (Recommended)
- **DigitalOcean**: [Deployment Guide](docs/DEPLOYMENT.md)
- **VPS/Docker**: [VPS Setup Guide](docs/VPS_QUICK_START.md)

---
[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com?referralCode=AHRe-w)

## ⌨️ Cursor/VS Code Keyboard Shortcuts

We have configured custom keyboard shortcuts (F1-F7) to quickly manage and execute common repository tasks directly within the **Cursor** or **VS Code** IDE.

These shortcuts map to predefined tasks in `.vscode/tasks.json` and are bound in `.vscode/keybindings.json`.

| Key | Action | Command Executed |
|-----|--------|------------------|
| **F1** | Run GenX Unified CLI | `python genx_unified_cli.py` |
| **F2** | Stop GenX Unified CLI | `pkill -f genx_unified_cli.py` |
| **F3** | Run GenX 24/7 Service | `python genx_24_7_service.py` |
| **F4** | Stop GenX 24/7 Service | `pkill -f genx_24_7_service.py` |
| **F5** | Run GenX 24/7 Backend | `python genx_24_7_backend.py` |
| **F6** | Stop GenX 24/7 Backend | `pkill -f genx_24_7_backend.py` |
| **F7** | Sync and Push to GitHub | `./SYNC-AND-PUSH-GITHUB.bat` |

### 🖱️ Programmatic Keyboard & Mouse Access
If you need programmatic control or automation of the keyboard and mouse (for example, GUI interactions or MT4/MT5 automation), please refer to `scripts/utils/keyboard_mouse_utils.py` which demonstrates usage of the `pynput` library. *Note: this requires a desktop/GUI environment to run properly.*
