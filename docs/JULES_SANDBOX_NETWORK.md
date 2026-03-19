# Jules Intelligent Community & Sandbox Networking System

This document outlines the architecture of the **Jules Sandbox Network**, an interconnected web of micro-environments functioning as a unified networking system operation.

## 🏗️ Architecture Overview

The system is defined via `docker-compose.sandbox.yml` and is composed of multiple isolated "sandboxes" communicating securely across a custom Docker bridge network (`jules-intelligent-community-net`). This setup ensures high availability, strict isolation, and real-time connectivity across the Jules ecosystem.

### Sandbox Nodes (Boxes)

#### 1. `jules-api-core-sandbox` (The Core)
*   **Role**: The central nervous system. Hosts the main FastAPI backend containing the ML models, scalping logic, and Okta-secured endpoint configurations (`Jules API`).
*   **Networking**: Exposed on port `8000` to the host, but accessible internally via `http://jules-api-core:8000`.
*   **Keep-Alive**: Configured with a Docker `healthcheck` ensuring continuous availability.

#### 2. `webapp-sandbox-primary` (Sandbox 1)
*   **Role**: The primary frontend integration point. Runs the React/Vite-based application (or Node.js integration) for end-users and AI agent roleplay interfaces.
*   **Networking**: Exposed on port `3000`. Connects directly to the Core via the `JULES_API_URL` environment variable.

#### 3. `webapp-sandbox-analytics` (Sandbox 2)
*   **Role**: A secondary frontend layer dedicated to analytics, system monitoring dashboards (Grafana-style data aggregation), and specific trading analysis visualizations.
*   **Networking**: Exposed on port `3001` to prevent port collisions with the primary sandbox.

#### 4. `mql5-forge-sandbox` (Trading / Git Integration)
*   **Role**: A specialized Alpine-based sandbox that bridges the gap between MetaQuotes Language 5 (MQL5) Expert Advisors and the centralized Git repository (`https://forge.mql5.io/LengKundee/mql5.git`).
*   **Integration**: Mounts the local `./expert-advisors` directory to `/mql5-workspace`. It pulls/pushes MQL5 source code, ensuring the community has the latest algorithmic updates.
*   **JetBrains Context**: In JetBrains IDEs (e.g., CLion, IntelliJ), this sandbox's mounted volume (`./expert-advisors`) serves as the working directory, allowing intelligent code completion and seamless containerized git operations.

#### 5. `jules-networking-monitor` (The Keep-Alive Ping Node)
*   **Role**: Ensuring "the system stays alive". This node continually polls the `jules-api-core-sandbox`. If the core fails, the monitor logs the unreachability, aiding in auto-recovery mechanisms or alerting.

## 🤝 The JetBrains Intelligent Community Integration

This sandbox architecture seamlessly integrates with the **JetBrains plugin ecosystem**:
1.  **Remote Interpreters/Docker Integration**: Using JetBrains tools (PyCharm, WebStorm), developers can configure the Docker Compose file (`docker-compose.sandbox.yml`) as a remote development target. The IDEs intelligently map the local codebase into the isolated sandbox environments.
2.  **MQL5 & C++ Tools**: The `./expert-advisors` mount allows JetBrains C++ tools to provide static analysis for `.mq5` files while the underlying `mql5-forge-sandbox` handles the `git push`/`pull` operations directly to the MQL5 Forge platform.
3.  **Ghost File Mitigation**: The IDEs are configured to ignore `.pyc`, `__pycache__`, and `node_modules` generated *within* the containers to prevent local workspace bloat (so we don't "gain weight" or get confused by overlapping dependencies).

## 🚀 Running the System

To boot the entire networking operation, use:
```bash
docker-compose -f docker-compose.sandbox.yml up -d
```

To view the health of the system and see the sandboxes talking:
```bash
docker-compose -f docker-compose.sandbox.yml logs -f jules-sys-monitor
```
