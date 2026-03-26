# GenX VisionOps — Architecture Blueprint 🚀

## 1. Intelligence Layer: Central Brain (brain/)
The global orchestration layer responsible for high-level intelligence and coordination.

### Core Modules:
- **Node Orchestrator**: Lifecycle and health management of the distributed node cluster.
- **Strategy AI**: Dynamic deployment of trading models (SMC, Trend) based on market volatility.
- **Risk AI**: Autonomous protection for drawdown monitoring and emergency shutdown.
- **AI Prompt Manager**: Templated interface for structured LLM communication (Gemini).

## 2. Execution Layer: Distributed Nodes (nodes/)
Decentralized workers optimized for high-performance market interaction.

### Active Nodes:
- **Forex Node**: Integrated with MetaTrader 5 (MT5) for Exness broker routing.
- **Crypto Node**: Optimized for Bybit API spot and derivatives trading.

## 3. Mission Control & Applets
- **React Dashboard**: High-performance port 3000 monitoring interface (located in `src/`).
- **Shader Pilot**: Bundled 3D world navigation tool for complex data interaction.
- **Telemetry**: Real-time health tracking via Socket.io and alerting via Telegram.

## 4. Shared & Integrations
- **Shared Utilities (`shared/`)**: Universal network bridges and system utilities.
- **Market Data (`integrations/`)**: Real-time price feeds and broker connectivity.
- **Alerting (`integrations/`)**: Telegram bot for global system notifications.
- **External APIs**: GitHub Master API integration for repository management and automated synchronization.
- **Jules AI Orchestrator**: Continuous deployment and monitoring logic for cloud-based execution.

## 5. Deployment Model
- **Backend**: Distributed Python orchestration logic.
- **Frontend**: React SPA with Express backend.
- **Continuous Execution**: Managed by `pm2` via `jules-deploy.sh`.

---
*Autonomous AI Trading Network — Season 2 Finalization.*
