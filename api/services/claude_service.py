"""
Claude AI Service for GenX Trading Platform
"""

import logging
import os
from typing import Any, Dict, List, Optional

import anthropic

from ..config import get_settings

logger = logging.getLogger(__name__)


class ClaudeService:
    """
    A service for interacting with the Anthropic Claude AI, particularly Claude Opus 4.6.

    Supports both standard Anthropic API and Azure OpenAI/Anthropic proxy configurations.
    """

    def __init__(self):
        """
        Initializes the ClaudeService.

        Configures the client based on provided environment variables.
        """
        self.settings = get_settings()
        self.client: Optional[anthropic.AsyncAnthropic] = None
        self.model_name = "claude-opus-4-6"
        self.initialized = False

    async def initialize(self) -> bool:
        """
        Asynchronously initializes the Claude client.

        Returns:
            bool: True if initialized successfully, False otherwise.
        """
        try:
            api_key = self.settings.ANTHROPIC_API_KEY
            azure_key = self.settings.AZURE_ANTHROPIC_API_KEY
            azure_endpoint = self.settings.AZURE_ANTHROPIC_ENDPOINT

            if azure_key and azure_endpoint:
                logger.info("Initializing Claude Service via Azure configuration.")
                # When using Azure, the endpoint and key are configured slightly differently.
                # For standard anthropic library proxy to azure, base_url is typically modified.
                self.client = anthropic.AsyncAnthropic(
                    api_key=azure_key,
                    base_url=azure_endpoint
                )
                self.initialized = True
            elif api_key:
                logger.info("Initializing Claude Service via standard Anthropic configuration.")
                self.client = anthropic.AsyncAnthropic(
                    api_key=api_key
                )
                self.initialized = True
            else:
                logger.warning("No Anthropic or Azure API keys found in configuration.")
                return False

            return True
        except Exception as e:
            logger.error(f"Failed to initialize Claude Service: {str(e)}")
            return False

    async def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Generates text using Claude Opus 4.6.

        Args:
            prompt (str): The input prompt.
            max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 1000.

        Returns:
            str: The generated response.
        """
        if not self.initialized or not self.client:
            logger.error("Claude Service not initialized.")
            return "Error: Service not initialized."

        try:
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error generating text with Claude: {str(e)}")
            return f"Error: {str(e)}"

    async def chat_analysis(self, messages: List[Dict[str, str]], max_tokens: int = 1024) -> str:
        """
        Performs analysis given a history of messages.

        Args:
            messages (List[Dict[str, str]]): A list of message dicts (e.g., {"role": "user", "content": "..."})
            max_tokens (int, optional): Maximum tokens. Defaults to 1024.

        Returns:
            str: The response text.
        """
        if not self.initialized or not self.client:
            logger.error("Claude Service not initialized.")
            return "Error: Service not initialized."

        try:
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error in chat analysis with Claude: {str(e)}")
            return f"Error: {str(e)}"

    async def health_check(self) -> bool:
        """
        Check if the service is configured and responsive.
        """
        if not self.initialized:
            return False

        try:
            # Send a tiny message to verify connectivity
            await self.client.messages.create(
                model=self.model_name,
                max_tokens=10,
                messages=[
                    {"role": "user", "content": "Ping"}
                ]
            )
            return True
        except Exception as e:
            logger.error(f"Claude health check failed: {str(e)}")
            return False

    async def shutdown(self):
        """
        Gracefully shutdown the client.
        """
        if self.client:
            await self.client.close()
            self.client = None
            self.initialized = False
