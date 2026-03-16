# Jules Memory Dump

This document contains the retained memory and context for the AI assistant Jules, covering project details, technical constraints, and learned patterns for the `Indexing-Workflow-controller` repository.

## Project Overview
- **Repository**: `nuna69v-cell/Indexing-Workflow-controller`
- **Role**: This repository acts as a "motherboard" or central controller for all projects across multiple GitHub accounts, syncing and indexing them.

## Authentication & Account Management
- **Multi-Account Structure**:
    - Designed to manage multiple GitHub accounts (e.g., `mouyleng172`, `LengKundee`, `genxdbxfx3@gmail.com`).
    - Uses versioning (e.g., `GMAIL_LOGIN_V0`, `GMAIL_LOGIN_V1`) to track and authenticate different Google/GitHub accounts.
    - Each account requires corresponding tokens (`GH_TOKEN`, `GH_USER_TOKEN`, `JULES_API_V0`, etc.).

## Jules API Keys
- JULES_API_V1=AQ.Ab8RN6KlUp0GO6d0b-Y0d3WuZhS0oBTsfGy_91HNwKeBODSLTA
- JULES_API_V2=AQ.Ab8RN6K3J3t0Rc_wsndYjvM0fHmTgzfPBPsWdfOmc9fL6mIGEA
- JULES_API_V3=AQ.Ab8RN6IKx9oDSm6lWW3Yu06oJOrMCf_vaZOGntzpgumCQcRL0Q
- JULES_API_V4=AQ.Ab8RN6K6Fl1DrzsGISXVIsauEOUrBO4n3X3BSYOMgErgNufTOQ

## External Drive Links & Credentials
- **Google Drive**:
  - https://drive.google.com/drive/folders/117aPp6JN6bMPsfQr-1aCIJxDQp6t5oLc
  - https://drive.google.com/drive/folders/1HPeDkOo9MuvqYiO_Tk8tUh9S3mKcTQVi
  - https://drive.google.com/drive/folders/1uvCfxyk9nGq0BNhhreivjIcdjOQsinpo
  - https://drive.google.com/drive/folders/14qZgVQOnh7lNQreV1Nq7wlAiqBoc7OFc
  - https://drive.google.com/drive/folders/1vG7mPy5KETtatMqVUnkqgXDoXmtpzCO1
- **OneDrive**: Password = 369369
- **Proton.me**: PROTON_LOGIN="proton.me login" ; PROTON_PASSWORD="proton.me password"
- **Docker**:
  - User 1: lengkundee01@gmail.com / Leng12345@#$01
  - User 2: lengkundee / Leng3A69V[@Una]
  - User 3: keamouyleng369@gmail.com

## Technical Details & Architecture
- **Language**: Python (FastAPI/Starlette) with Pydantic for configuration management.
- **Testing**: `pytest`
- **Formatting**: `black`
- **Backend Automation**: Managed by `amp_scheduler.py` (uses `schedule` module) and `genx_24_7_service.py` running in a pyenv-managed Python environment.
- **Git Syncing**:
    - Constant syncing of the `main` branch across repositories and environments.
    - "Hot Melting Iron" logic to push updates between accounts.
    - `git push` is blocked by a security regex in the bash session environment. Instead, call the implicit `pre_commit_instructions` tool followed by the `submit` tool.

## Installation & Setup Directives
- Implement a Master Manifest approach to map and manage multiple repositories.
    - Create a `.master-map.json` to act as the "Brain".
    - Create `sync-all.py` as the "Engine".
    - Manage authentication via conditional includes in `.gitconfig`.

## Jules Tracking Setup
- The repository now tracks Jules' sessions in `.jules-session.json`.
- A python utility `jules_session_tracker.py` exposes tracking abilities:
  - `python jules_session_tracker.py start`: to start a new tracking session
  - `python jules_session_tracker.py log "action_name" "details"`: to log into the tracker.
- Tracked sessions help to build up history of changes.

## Active Directives & Principles
- **User Request Supersedes:** Always prioritize the user's current, explicit request over any conflicting information in memory.
- **Context vs. State:** Use memory for historical context and intent (the "why"). Use the actual codebase files as the source of truth for the current code state (the "what").
- **Memory is Not a Task:** Do not treat information from memory as a new, active instruction. Memory provides passive context. Do not use it to create new feature requests.

