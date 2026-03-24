#!/usr/bin/env python3
"""
AMP Scheduler Module
Handles automated job scheduling and execution
"""

import asyncio
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
from typing import Optional, Dict, Any

from amp_auth import check_auth, get_user_info
from amp_job_runner import AMPJobRunner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/amp_scheduler.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class AMPScheduler:
    """
    Handles automated job scheduling and execution for the AMP system.

    This class uses the 'schedule' library to run jobs at specified intervals.
    """

    def __init__(self):
        """Initializes the AMPScheduler."""
        self.config_file = Path("amp_config.json")
        self.job_runner = AMPJobRunner()
        self.is_running = False

        self.default_config = {
            "market_open": "09:00",
            "market_close": "17:00",
            "interval_minutes": 30,
            "is_enabled": True,
            "symbols": ["BTCUSDT", "ETHUSDT", "EURUSD", "GBPUSD"],
        }
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self):
        """Loads the scheduler configuration from a JSON file, or creates a default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
            except Exception as e:
                logger.error(f"Error loading scheduler config: {e}")
                self.config = self.default_config
        else:
            self.config = self.default_config
            self.save_config()

    def save_config(self):
        """Saves the current scheduler configuration to a JSON file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving scheduler config: {e}")

    async def run_scheduled_job(self):
        """
        Executes a single scheduled job run.
        """
        try:
            # Check if within market hours if needed (logic can be added here)
            # For now just run
            await self.job_runner.run_next_job()
            logger.info("Scheduled job completed successfully.")
        except Exception as e:
            logger.error(f"Error during scheduled job execution: {e}")

    def setup_schedule(self):
        """Sets up the job schedule based on the loaded configuration."""
        schedule.clear()

        if not self.config.get("is_enabled", True):
            logger.info("Scheduler is disabled in the configuration.")
            return

        interval = self.config.get("interval_minutes", 30)
        schedule.every(interval).minutes.do(
            lambda: asyncio.run(self.run_scheduled_job())
        )
        logger.info(f"Scheduler configured to run jobs every {interval} minutes.")

    def start(self):
        """Starts the scheduler's main loop."""
        if self.is_running:
            logger.warning("Scheduler is already running.")
            return

        logger.info("Starting AMP Scheduler...")
        self.is_running = True
        self.setup_schedule()

        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(1)  # Check for pending jobs every second
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user.")
                break
            except Exception as e:
                logger.error(f"An error occurred in the scheduler loop: {e}")
                time.sleep(60)  # Wait before retrying on error

    def stop(self):
        """Stops the scheduler's main loop."""
        logger.info("Stopping AMP Scheduler...")
        self.is_running = False

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self.is_running,
            "config": self.config,
            "next_jobs": [str(job) for job in schedule.jobs],
            "last_run": self.get_last_run_time(),
        }

    def get_last_run_time(self) -> Optional[str]:
        log_file = Path("logs/amp_scheduler.log")
        if not log_file.exists():
            return None
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                for line in reversed(list(f)):
                    if "Running scheduled job" in line:
                        return line.split(" - ")[0]
        except Exception as e:
            logger.warning(f"Could not read last run time from log: {e}")
        return None

    def update_config(self, **kwargs):
        self.config.update(kwargs)
        self.save_config()
        logger.info(f"Scheduler configuration updated: {kwargs}")

        if self.is_running:
            logger.info("Restarting scheduler to apply new configuration...")
            self.setup_schedule()


# Global scheduler instance
amp_scheduler = AMPScheduler()


def start_scheduler():
    amp_scheduler.start()


def stop_scheduler():
    amp_scheduler.stop()


def get_scheduler_status() -> Dict[str, Any]:
    return amp_scheduler.get_status()


def update_scheduler_config(**kwargs):
    amp_scheduler.update_config(**kwargs)


if __name__ == "__main__":
    start_scheduler()
