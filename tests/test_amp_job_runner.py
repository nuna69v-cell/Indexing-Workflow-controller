import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from amp_job_runner import AMPJobRunner

def test_load_config_success():
    """Test that load_config successfully loads a valid JSON file."""
    mock_data = {"api_provider": "test_provider", "enabled_services": ["service1"]}
    mock_json = json.dumps(mock_data)

    with patch.object(Path, "exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=mock_json)):
        runner = AMPJobRunner()
        config = runner.load_config()
        assert config == mock_data

def test_load_config_file_not_found():
    """Test the fallback behavior when config file is not found (FileNotFoundError)."""
    with patch.object(Path, "exists", return_value=True), \
         patch("builtins.open", side_effect=FileNotFoundError):
        runner = AMPJobRunner()
        config = runner.load_config()
        assert config == {}

def test_load_config_file_not_exists():
    """Test the fallback behavior when config file does not exist (exists() returns False)."""
    with patch.object(Path, "exists", return_value=False):
        runner = AMPJobRunner()
        config = runner.load_config()
        assert config == {}
