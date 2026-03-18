#!/bin/bash
# Deploy EA Host to Hostinger using Gemini CLI

# Ensure HOSTINGER_API_TOKEN is set
if [ -z "$HOSTINGER_API_TOKEN" ]; then
    echo "Error: HOSTINGER_API_TOKEN is not set."
    echo "Please export your Hostinger API Token:"
    echo "export HOSTINGER_API_TOKEN='your-token-here'"
    exit 1
fi

# Ensure GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY is not set."
    echo "Please export your Gemini API Key:"
    echo "export GEMINI_API_KEY='your-gemini-key-here'"
    exit 1
fi

echo "Starting EA Host deployment via Gemini and Hostinger MCP..."

# Instruct Gemini CLI to deploy the EA host using the Hostinger API
gemini -p "Use the Hostinger API MCP server to list available VPS instances, find an active one, and run a bash script on it to deploy the EA host. The EA host is a Python/Node.js application. You will need to clone the repository, install Python/Node dependencies, and start the application using 'genx_24_7_service.py' or 'npm run start:prod'. Ensure the VPS allows WebRequests on port 8000/3000." --yolo

echo "Deployment request sent to Gemini."
