# Claude Opus 4.6 Setup Guide

This guide explains how to set up the GenX Trading Platform to use the **Claude Opus 4.6** model from Anthropic, including support for Microsoft Azure AI Catalog deployments.

## Overview
The platform uses the `anthropic` Python SDK to communicate with Claude models. `ClaudeService` located at `api/services/claude_service.py` manages these interactions.

## 1. Prerequisites
Ensure you have updated your Python environment to include the required dependencies:
```bash
pip install -r requirements.txt
```

## 2. Configuration
You can configure Claude using either a standard Anthropic API key or through Azure AI Foundry.

### Option A: Standard Anthropic API
1. Obtain an API key from the [Anthropic Console](https://console.anthropic.com/).
2. Add the following to your `.env` file:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Option B: Azure AI Foundry (Microsoft Azure)
If you are deploying Claude Opus 4.6 via the [Azure AI Model Catalog](https://ai.azure.com/catalog/models/claude-opus-4-6):
1. Deploy the model in your Azure AI Foundry portal.
2. Obtain the endpoint URL and the API key.
3. Add the following to your `.env` file:
```env
AZURE_ANTHROPIC_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_ANTHROPIC_API_KEY=your_azure_api_key_here
```

*Note: The system automatically prioritizes the Azure configuration if both `AZURE_ANTHROPIC_ENDPOINT` and `AZURE_ANTHROPIC_API_KEY` are provided.*

## 3. Usage
The `ClaudeService` is designed to work asynchronously within the FastAPI application:

```python
from api.services.claude_service import ClaudeService

async def example_usage():
    claude = ClaudeService()
    success = await claude.initialize()
    if success:
        response = await claude.generate_text("What is the current market sentiment?", max_tokens=1000)
        print(response)
    await claude.shutdown()
```

## Troubleshooting
- **ModuleNotFoundError: No module named 'anthropic'**: Make sure you have installed the required dependencies using `pip install anthropic>=0.21.3`.
- **Initialization Fails**: Ensure your `.env` file is properly formatted and loaded by `api/config.py`.
