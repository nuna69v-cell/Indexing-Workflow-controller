import pytest
import os
from unittest.mock import patch
from scripts.utils.underground_worker import UndergroundWorker

def test_underground_worker_init():
    with patch.dict(os.environ, {"JULES_API_V1": "test_api_key"}):
        worker = UndergroundWorker()
        assert worker.jules_api == "test_api_key"

def test_underground_worker_execute():
    worker = UndergroundWorker()
    result = worker.execute_remote_command("status")
    assert result["status"] == "success"
    assert "status" in result["message"]
