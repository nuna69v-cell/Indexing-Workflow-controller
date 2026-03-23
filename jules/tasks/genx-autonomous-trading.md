# GenX Autonomous Trading Network

Objective:
Build a multi-broker automated trading system connected to MT5 terminals for:

Broker 1:
Exness
Server: exness_mt5real24

Broker 2:
FxPro
Server: fxpro-mt5

The system must evolve from a simple bot into an autonomous trading network.

-----------------------------------

PHASE 1 — Core Trading Engine

Components:

1. Strategy Engine
- Moving Average trend system
- Breakout strategy
- Liquidity sweep detection

2. Risk Engine
- Risk per trade: 1%
- Maximum drawdown: 10%
- Maximum open trades: 5

3. Execution Engine
- Connect to MT5 terminal
- Send Buy / Sell orders
- Apply Stop Loss / Take Profit

4. Logging System
- Record every trade
- Save strategy results
- Save market data snapshots

-----------------------------------

PHASE 2 — Multi-Broker Execution

The system must support:

- Exness MT5 terminal
- FxPro MT5 terminal

Execution logic:

Strategy Signal
       ↓
Execution Router
   ↓         ↓
Exness MT5  FxPro MT5

Add latency measurement and spread comparison.

-----------------------------------

PHASE 3 — AI Strategy Evolution

Create a system that:

- stores trade results
- evaluates strategies
- replaces losing strategies
- improves winning strategies

Components:

Strategy Manager
Performance Analyzer
Model Optimizer

-----------------------------------

PHASE 4 — Autonomous Operation

The system must run continuously on VPS.

Features:

- auto restart
- health monitoring
- trade alerts
- performance dashboard

-----------------------------------

PHASE 5 — Signal Integration

Support external signals from:

TradingView alerts
Market data APIs

Signals must be processed through a webhook.

-----------------------------------

PHASE 6 — Self Learning System

Create a module that:

- analyzes historical trades
- finds profitable patterns
- generates new strategy parameters

-----------------------------------

Deliverables:

1. Python trading engine
2. MT5 execution bridge
3. multi-broker support
4. monitoring dashboard
5. VPS deployment guide
6. test suite


---

Repository Structure Jules Should Build

genx-autonomous-trading/

core/
engine.py
orchestrator.py

strategy/
trend_strategy.py
breakout_strategy.py
liquidity_strategy.py

risk/
risk_manager.py
drawdown_guard.py

execution/
mt5_executor.py
broker_router.py

brokers/
exness_mt5.py
fxpro_mt5.py

ai/
strategy_optimizer.py
performance_analyzer.py
pattern_discovery.py

data/
market_storage.py
trade_history.py

signals/
tradingview_webhook.py

monitor/
dashboard.py
telemetry.py

infra/
vps_setup.md
docker/

tests/

main.py
README.md


---

Core Architecture

Market Data
      ↓
Strategy Engine
      ↓
Risk Engine
      ↓
Execution Router
   ↓           ↓
Exness MT5   FxPro MT5


---

Autonomous Trading Network (Next Level)

Final system Jules should build:

AI Strategy Lab
      ↓
Strategy Optimizer
      ↓
Trading Engine
      ↓
Execution Router
   ↓          ↓
Exness      FxPro

System improvements:

• strategy performance scoring
• automatic strategy replacement
• risk monitoring
• trading statistics


---

Monitoring Dashboard

Jules should generate a dashboard that shows:

Account balance
Open trades
Win rate
Daily profit
Max drawdown
Strategy performance


---

VPS Deployment

Recommended architecture:

VPS

├ MT5 Terminal (Exness)
├ MT5 Terminal (FxPro)
├ Python Trading Engine
├ AI Strategy Optimizer
└ Monitoring Dashboard


---

Start With Free Resources

Use:

Demo account on Exness
Demo account on FxPro
Local computer or VPS
MT5 terminal
Python trading engine
Jules coding agent

Only move to live trading after strategy validation.


---

Expected Result

A fully automated system capable of:

generating trading signals

executing trades automatically

managing risk

improving strategies over time
