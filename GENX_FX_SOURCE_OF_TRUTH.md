# GenX FX Source of Truth

This document contains verified project details, technical constraints, and established patterns for the GenX FX Trading Platform.

## Project Context
- **Repository**: Hybrid trading system (Python/Node.js/React).
- **Core Technologies**:
    - **Backend**: Python FastAPI (`api/`), Node.js Express (`services/server/`).
    - **Database**: PostgreSQL (Drizzle ORM), MongoDB (AI training logs), Redis (Caching).
    - **Trading**: MetaTrader 5 (MT5), Bybit.
    - **Deployment**: Railway, Docker, Gitea Actions.

## Technical Standards
- **Asynchronicity**: Always use `asyncio` and `aiohttp` for I/O-bound tasks (data fetching, notifications).
- **Performance**:
    - Offload CPU-bound tasks (technical indicators, ML inference) to threads using `asyncio.to_thread`.
    - Use NumPy vectorization for technical indicators to avoid Pandas overhead.
- **Risk Management**:
    - Position sizing follows the formula: `Lot Size = (Account Balance * Risk %) / (Stop Loss Distance * Tick Value)`.
    - Automated news filter pauses trading 30m before/after high-impact events.
- **Security**:
    - EA endpoints require `X-API-Key` authentication.
    - Sensitive data encrypted using Fernet (`utils/encryption.py`).
- **Reliability**:
    - Wrap network and trading calls in the `@retry_async` decorator from `utils/retry_handler.py`.

## Verified File Structure
- `api/`: FastAPI backend.
- `core/`: Trading engine, risk management, and indicators.
- `expert-advisors/`: MQL4/MQL5 source files.
- `vps-config/`: Gitea runner and VPS setup scripts.
- `tests/`: Includes `walk_forward_test.py`.

## Maintenance
- Use `pnpm` for all JavaScript-related dependencies.
- Use `black` for Python formatting.
