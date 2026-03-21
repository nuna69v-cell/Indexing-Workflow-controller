# Memory Verification Report

This document classifies information from Jules's memory as TRUE or FALSE based on the current state of the repository.

| Memory Item | Status | Verification |
| :--- | :--- | :--- |
| Trademark attributions in 'NOTICE' file | **FALSE** | `NOTICE` file does not exist in the root. |
| Project supports automated deployment to Railway | **TRUE** | `railway.json` exists and `README.md` mentions it. |
| Trading system built with Python, MT5, Docker, MongoDB | **TRUE** | Confirmed usage in `utils/retry_handler.py`, `Dockerfile`, and `services/ai_trainer.py`. |
| Position sizing: Lot Size = (Account Balance * Risk %) / (Stop Loss Distance * Tick Value) | **TRUE** | Formula confirmed in `core/risk_management/position_sizer.py`. |
| Use asynchronous execution (asyncio and aiohttp) | **TRUE** | Extensively used across `api/` and `core/`. |
| Forgejo Migration automation via 'scripts/deployment/forgejo_migrate.py' | **FALSE** | File `scripts/deployment/forgejo_migrate.py` is missing. |
| Matrix (Element) notifications via 'services/matrix_bot.py' | **FALSE** | File `services/matrix_bot.py` is missing. |
| Application settings must be imported using 'from ..config import get_settings' | **PARTIAL** | `api/main.py` uses it, but many services don't directly. |
| News filter (NewsFilter) to pause signal generation | **TRUE** | `api/services/news_filter.py` exists. |
| Gitea Actions workflow '.gitea/workflows/deploy-vps.yml' | **TRUE** | File exists. |
| 'ONENOTE-GUIDE.md' is the master guide | **FALSE** | File `ONENOTE-GUIDE.md` is missing. |
| Walk-Forward Optimization in 'tests/walk_forward_test.py' | **TRUE** | File exists. |
| Forgejo runner integration via 'vps-config/setup_runner.sh' | **TRUE** | File exists. |
| Reliability Convention: @retry_async decorator in 'utils/retry_handler.py' | **TRUE** | File exists and contains retry logic. |
| Expert Advisor (EA) HTTP endpoints require 'X-API-Key' | **TRUE** | Confirmed in `api/utils/ea_auth.py`. |

## Cleaned up actions:
- Removed references to missing files: `NOTICE`, `scripts/deployment/forgejo_migrate.py`, `services/matrix_bot.py`, `ONENOTE-GUIDE.md`.
- Confirmed core trading and architecture principles.
