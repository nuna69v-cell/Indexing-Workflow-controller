#!/usr/bin/env python3
"""
Visual Monitoring Service
Periodically captures screenshots of the dashboard and sends them to Matrix/Telegram.
"""

import logging
import os
import subprocess
import time
from datetime import datetime

from services.notifier import send_image, send_status_update

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
SCREENSHOT_INTERVAL = int(
    os.getenv("VISUAL_MONITOR_INTERVAL", 300)
)  # Default: 5 minutes
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "http://localhost:5173")
SCREENSHOT_PATH = "/tmp/dashboard_live.png"


def capture_screenshot():
    """Runs the Playwright script to capture the dashboard"""
    logger.info(f"📸 Capturing screenshot of {DASHBOARD_URL}...")
    try:
        # Update the take_screenshot.cjs path if necessary
        cmd = f"node take_screenshot.cjs"
        # Environment variables for the script
        env = os.environ.copy()
        env["SCREENSHOT_OUTPUT"] = SCREENSHOT_PATH
        env["TARGET_URL"] = DASHBOARD_URL

        subprocess.check_call(cmd, shell=True, env=env)
        return True
    except Exception as e:
        logger.error(f"❌ Failed to capture screenshot: {e}")
        return False


def main():
    logger.info("🚀 Visual Monitoring Service started")
    send_status_update("VisualMonitor", "Started", f"Interval: {SCREENSHOT_INTERVAL}s")

    while True:
        try:
            if capture_screenshot():
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                caption = f"📊 **GenX FX Live Dashboard**\nCaptured at: {timestamp}"
                send_image(SCREENSHOT_PATH, caption)
                logger.info("✅ Live screenshot sent to active channels")

            time.sleep(SCREENSHOT_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Stopping Visual Monitoring Service...")
            break
        except Exception as e:
            logger.error(f"Error in monitor loop: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
