# AI Agent Plugins Configuration

This directory contains configuration and documentation for AI agent plugins used in the project.

## Available Plugins

### 1. Jules Agent (Google AI)
- **Purpose**: Trading automation, code review, and merge automation
- **Provider**: Google AI Studio
- **Configuration**: `jules-agent-config.json`
- **Documentation**: `JULES-AGENT.md`

### 2. Qodo Plugin
- **Purpose**: Code quality and testing
- **Provider**: Qodo
- **Configuration**: `qodo-config.json`
- **Documentation**: `QODO-PLUGIN.md`

### 3. Cursor Agent
- **Purpose**: AI-assisted code editing
- **Provider**: Cursor AI
- **Configuration**: `.cursor/rules/`
- **Documentation**: `CURSOR-AGENT.md`

### 4. Kombai Agent
- **Purpose**: Design to code conversion
- **Provider**: Kombai
- **Configuration**: `kombai-config.json`
- **Documentation**: `KOMBAI-AGENT.md`

## Setup Instructions

1. Review the documentation for each plugin in their respective `.md` files
2. Configure API keys and settings in the corresponding config files
3. Never commit API keys or secrets - use environment variables or Windows Credential Manager
4. Test each plugin individually before enabling all automations

## Security Notes

- All API keys should be stored in environment variables or Windows Credential Manager
- Config files with sensitive data are gitignored
- Use `.env.example` as a template for your local `.env` file
