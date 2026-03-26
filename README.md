# GenX VisionOps — Autonomous AI Trading Network 🏁

## Overview
GenX VisionOps is a distributed **Autonomous AI Trading Network**. It has evolved into a production-grade infrastructure for managing multi-market execution across Forex and Crypto environments.

## 🚀 Key Infrastructure
- **[Central Brain](./BRAIN_ARCHITECTURE.md)**: Intelligence & Global Orchestration.
- **Distributed Nodes**: Specialized execution workers for MT5 and Bybit.
- **Mission Control**: React Dashboard (Port 3000) & Socket.io Telemetry.
- **System Readiness**: Fully verified, telemetry-enabled, and production-ready.

## 📂 Production Layout
```text
.
├── brain/                # Central Intelligence & Orchestrator
├── nodes/                # Distributed Execution Workers
├── shared/               # Universal Bridges & Network Utilities
├── integrations/         # Market Data & Telegram Alerting
├── src/                  # Mission Control (React / Port 3000)
└── tests/                # Unified System Verification Suite
```

## 🔧 Operation
- **Full Setup**: Run `./setup.sh` (Linux/macOS) or `.\setup.ps1` (Windows)
- **Start Network**: Run `./start.sh` (Linux/macOS) or `.\start.ps1` (Windows)
- **Continuous Deployment**: Run `./jules-deploy.sh` (Linux/macOS) to start via PM2.
- **Manual Start**: `npm run dev` (Central Brain) and `python3 main.py` (Orchestrator)
- **Verify Health**: `python3 -m unittest discover tests/`
- **Dashboard**: `http://localhost:3000`

## 🤝 Collaboration & Sync
- **GitHub Action**: The `.github/workflows/collaborate.yml` handles synchronization between the main repository, MQL5 Forge, and Codeberg.
- **Repositories**:
  - Main: `https://github.com/nuna69v-cell/ZOLO-A6-9VxNUNA-GenX.git`
  - Forge: `https://forge.mql5.io/nuna/forgeMQL5.git`
  - Codeberg: `https://codeberg.org/LengKundee/ZOLO-A6-9VxNUNA-GenX.git`
  - GitHub Master API: `https://api.github.com/`

---
*Created and managed by Jules AI.*

### 📱 Mobile Mission Control
Control your trading network from anywhere:
- **PWA Ready**: Install directly from Chrome/Edge on Android/iOS.
- **Features**: Real-time node status, strategy switching, and emergency kill switch.
