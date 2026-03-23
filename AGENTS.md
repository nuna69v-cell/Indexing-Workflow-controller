# AGENTS

## 📓 Knowledge Base
- **NotebookLM (Primary)**: [Access here](https://notebooklm.google.com/notebook/e8f4c29d-9aec-4d5f-8f51-2ca168687616)
- **NotebookLM (Blueprint & Strategy)**: [Access here](https://notebooklm.google.com/notebook/da5f7773-bb49-40d5-975c-2a30fd6b37c3)
- **OneDrive Blueprint Notes**: [Quick Notes - Blueprint](https://onedrive.live.com/view.aspx?resid=8F247B1B46E82304%21s47a25b152cbc4de0986115d88145a225&id=documents&wd=target%28Quick%20Notes.one%7C8BA711F8-2F20-4E7B-80E6-8A8AE35E44EE%2F%F0%9F%9F%A6Blueprint%7C537850C8-5311-4245-998C-DF5B039E5053%2F%29&wdpartid={2A7121B3-322E-660B-0CE6-D3E30D3240A7}{1}&wdsectionfileid=8F247B1B46E82304!s1989476304ab43a4b1dec048cc4fe5ec)
- **Note**: These notebooks and OneDrive notes are available for reading and writing. AI agents must read them before starting work to understand the project context, strategies, and blueprints.


## Repository summary
- MQL5 indicator and Expert Advisor live in `mt5/MQL5/Indicators` and `mt5/MQL5/Experts`.
- Automation and deployment helpers live in `scripts/` with configuration in `config/`.
- Guides and references live in `docs/`.

## Key files and directories
- `mt5/MQL5/Indicators/SMC_TrendBreakout_MTF.mq5`
- `mt5/MQL5/Experts/SMC_TrendBreakout_MTF_EA.mq5`
- `scripts/startup_orchestrator.py`, `scripts/startup.ps1`, `scripts/startup.sh`
- `scripts/ci_validate_repo.py`, `scripts/test_automation.py`
- `config/startup_config.json`

## Local checks
- Repository validation: `python scripts/ci_validate_repo.py`
- Automation tests: `python scripts/test_automation.py`
- Package MT5 files: `bash scripts/package_mt5.sh`

## Manual validation
- Compile MQL5 files in MetaEditor and refresh in MT5.

## Jules Integration
- **Jules Task ID**: 11566195936388909103
- **Setup Guide**: [Jules Task Setup](docs/Jules_Task_Setup.md)
- **Setup Script**: `bash scripts/setup_jules_task.sh [TASK_ID]`
- Jules CLI requires authentication via `jules login` before pulling tasks

## Notes
- Keep generated artifacts (logs, `dist/`, caches) out of version control.
- If behavior changes, update the relevant docs under `docs/`.

## Persona and Goal
You are an expert Quant Trader. Your goal is to maintain a Python trading bot using the ccxt library for OKX and MetaTrader5 for FxPro. You must optimize for low drawdown and 24/7 uptime.
