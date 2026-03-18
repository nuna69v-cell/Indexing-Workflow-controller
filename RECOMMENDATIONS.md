# GenX_FX System Recommendations & Restructuring

Based on the recent changes to integrate IP, Port mapping, and Jules API key injection into the EA configurations, here is a status summary and my recommendations for the project structure.

## 1. Package Manager & Port Mapping
We have updated `scripts/utils/manage_packages.py` to include a new function `map_ea_environments`.
This function creates an `ea_port_mapping.json` file which defines dynamic IPs, auto-incrementing Ports (starting at 5555), and automatically allocates Jules API keys found in the system's environment variables.
The mapping allows the platform to run multiple EA variants simultaneously without port conflicts.

## 2. Expert Advisors Updates
Both the MT4 and MT5 EAs (`expert-advisors/mt4_ea/GenZTradingEA.mq4` and `expert-advisors/mt5_ea/GenZTradingEA.mq5`) have been restructured. They no longer rely on a static string for `ServerURL`. Instead, they dynamically construct their endpoint from specific `IPAddress` and `Port` inputs, and natively support an `API_KEY` parameter which is appended as a Bearer token in the `WebRequest` headers.

## 3. Recommended Repository Restructuring
Currently, the codebase contains multiple top-level scripts and directories, some of which are very large and duplicate functionality (e.g., `genx_24_7_backend.py` vs `genx_robust_backend.py`, or scattered setup scripts in `/scripts`, root dir, and `/windows-setup`).

### Recommendations:
1. **Consolidate Backend Entry Points:** Select a single backend implementation (e.g., `api/main.py`) and deprecate or move experimental Python backends to an `/experimental` folder.
2. **Centralize Deployment Scripts:** Scripts like `setup-and-run-all.ps1`, `launch-docker.bat`, and `jules_setup.sh` should be unified in a `/deployment` or `/scripts/deploy` directory to reduce root clutter.
3. **Environment Isolation:** Ensure `.env` files are fully respected. The `manage_packages.py` script now looks for `JULES_API_V*` or `GH_TOKEN` directly from the OS variables. Make sure your `.env` loader correctly populates `os.environ`.
4. **EA API Keys:** To fully automate EA injection from Python, consider creating a script that parses the `ea_port_mapping.json` and updates the `input string API_KEY = "JULES_API_KEY_HERE"` defaults in the `.mq4/.mq5` source files dynamically before compiling them.

## 4. How to Apply
To apply the new port mapping:
1. Run `python3 scripts/utils/manage_packages.py`
2. Review the generated `ea_port_mapping.json`.
3. Open the EA in MetaEditor, note the new `IPAddress`, `Port`, and `API_KEY` inputs, and configure them matching the mapping output.
