# GenX_FX Trading System

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com?referralCode=AHRe-w)
[![CI Workflow](https://github.com/Mouy-leng/genx-trading/actions/workflows/ci.yml/badge.svg)](https://github.com/Mouy-leng/genx-trading/actions/workflows/ci.yml)
[![Copilot Setup Steps](https://github.com/Mouy-leng/genx-trading/actions/workflows/copilot-setup-steps.yml/badge.svg)](https://github.com/Mouy-leng/genx-trading/actions/workflows/copilot-setup-steps.yml)

Advanced AI-Powered Forex Signal Generator for MT4/5 Expert Advisors and fully automated algo-trading using `ccxt` and `backtrader`.

## 🚀 Overview
GenX_FX is a comprehensive, production-ready trading platform that combines a Python FastAPI backend for AI-powered predictions and market analysis with a Node.js Express server and React frontend for user interaction. It also incorporates strong Python-based backtesting.

## ✨ Features
- **AI-Powered Predictions**: Leverages machine learning models for high-probability trading signals.
- **Backtesting Engine**: Uses `backtrader` for robust historical testing of trading strategies (e.g., RSI/MACD).
- **Hybrid Architecture**: Combines Python's data processing power with Node.js's scalability.
- **MT4/MT5 Integration**: Seamlessly connects with MetaTrader Expert Advisors via CSV and API.
- **Real-time Monitoring**: Integrated dashboard for tracking account performance and system health.
- **Robust Risk Management**: Automated position sizing and risk controls.

## 📂 Project Structure
- `src/mouy_leng/trading/`: Core automated trading strategies and backtesting.
- `tests/`: Pytest suite aiming for >80% coverage.
- `api/`: Python FastAPI backend.
- `client/`: React + TypeScript frontend.
- `services/server/`: Node.js Express proxy and static file server.
- `core/`: Core trading logic and strategies.
- `expert-advisors/`: MetaTrader EA source files.
- `docs/`: Comprehensive documentation and deployment guides.
- `.github/`: CI workflows and Copilot rules.

## 🛠️ Getting Started
### Local Setup (Trading Algos)
1. Set Python version (3.13+ recommended): `pyenv local 3.13`
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `PYTHONPATH=. pytest`
4. Run backtest: `python -m src.mouy_leng.trading.backtest`

For general backend/frontend setup, please refer to:
- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Comprehensive Documentation](docs/COMPREHENSIVE_DOCUMENTATION.md)

## 🚢 Deployment
GenX_FX is designed for easy deployment on modern cloud platforms:
- **Railway**: [Railway Deployment Guide](docs/RAILWAY_DEPLOYMENT.md) (Recommended)
- **DigitalOcean**: [Deployment Guide](docs/DEPLOYMENT.md)
- **VPS/Docker**: [VPS Setup Guide](docs/VPS_QUICK_START.md)

## 🤖 GitHub Copilot Rules
Check out `.github/copilot-instructions.md` for the strict AI assistant constraints configured for this environment.
