# Hostinger EA Host Deployment

This repository includes a script to deploy the EA Host to Hostinger using the Gemini CLI.

## Prerequisites

1.  **Hostinger API Token:** You need an API token from your Hostinger account.
2.  **Gemini API Key:** You need a Gemini API Key to use the `gemini` CLI.

## Setup

1.  Export your API keys:
    ```bash
    export HOSTINGER_API_TOKEN="your_hostinger_token_here"
    export GEMINI_API_KEY="your_gemini_key_here"
    ```

2.  Run the deployment script:
    ```bash
    ./deploy-hostinger.sh
    ```

The script will use the Gemini CLI along with the `hostinger-api-mcp` to list your Hostinger VPS instances and attempt to deploy the Python/Node.js backend required for the Expert Advisor to connect.

Make sure your EA in MT5 has the correct URL pointing to the deployed Hostinger VPS IP or domain.
