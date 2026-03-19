# Docker Deployment and "Getting Started" Plan for GUI Terminal

## Overview
This plan outlines how to deploy the GenX Indexing-Workflow-controller with an integrated, containerized `ttyd` GUI Terminal. This setup will give AI agents and users a web-based terminal interface inside the deployment environment.

## 1. Prerequisites
- Docker and `docker-compose` installed.
- Ensure ports `8000` (FastAPI backend) and `7681` (GUI Terminal) are open/accessible.

## 2. Updated Architecture Summary
The deployment now includes a `gui_terminal` service configured in `docker-compose.yml`:
- **Base image:** Reuses the environment defined in the root `Dockerfile`.
- **Port mapping:** Exposes the terminal on `7681:7681`.
- **Entrypoint:** `start_gui_terminal.sh` script, which launches `ttyd -p 7681 bash` inside the container.
- **Integration:** The `ttyd` installation and setup is automated via `jules_setup.sh`.

## 3. Getting Started Guide

### Step 1: Clone and Configure
Clone the repository and set up your `.env` file based on `.env.example`. Make sure you have the necessary API keys defined (e.g. Bybit, OpenAI, etc. if needed).

```bash
git clone https://github.com/nuna69v-cell/Indexing-Workflow-controller.git
cd Indexing-Workflow-controller
```

### Step 2: Build and Run via Docker Compose
To launch the entire platform, including the API backend, scheduled bots, and the new GUI terminal, run:

```bash
docker-compose up --build -d
```

### Step 3: Accessing the Services
Once the containers are successfully running, you can access the services:
- **FastAPI Backend (Swagger UI):** http://localhost:8000/docs
- **GUI Terminal:** http://localhost:7681

### Step 4: AI Agent Collaboration
The web terminal gives all Jules AI (or other collaborative agents) an interactive bash shell running in the same networked environment as the backend services. They can execute scripts, view real-time logs, or manage configurations directly via the `gui_terminal` service container.

## Next Steps / Notes on Images
The images attached (IMG_20260319_222044_864.jpg, IMG_20260319_222206_166.jpg) depict system/terminal status context. By utilizing the `docker-compose` setup above, the exact runtime environment is captured, matching the setup expected in the reference materials, and mitigating platform-specific dependency issues.
