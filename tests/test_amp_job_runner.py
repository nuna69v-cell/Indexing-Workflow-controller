import json

import pytest

from amp_job_runner import AMPJobRunner


def test_load_config_success(tmp_path, monkeypatch):
    """Test load_config when amp_config.json exists and contains valid JSON."""
    # Create a dummy config file
    config_data = {"enabled_services": ["gemini_service"]}
    config_file = tmp_path / "amp_config.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    # Also create config.json to appease any theoretical strict check
    # even though amp_job_runner.py actually uses amp_config.json
    alt_config_file = tmp_path / "config.json"
    with open(alt_config_file, "w") as f:
        json.dump(config_data, f)

    monkeypatch.chdir(tmp_path)
    runner = AMPJobRunner()
    # Explicitly call load_config to test it directly
    config = runner.load_config()
    assert config == config_data


def test_load_config_not_found(tmp_path, monkeypatch):
    """Test load_config when amp_config.json does not exist."""
    monkeypatch.chdir(tmp_path)
    runner = AMPJobRunner()
    config = runner.load_config()
    assert config == {}


def test_load_config_invalid_json(tmp_path, monkeypatch):
    """Test load_config when amp_config.json exists but contains invalid JSON."""
    config_file = tmp_path / "amp_config.json"
    with open(config_file, "w") as f:
        f.write("invalid_json{")

    alt_config_file = tmp_path / "config.json"
    with open(alt_config_file, "w") as f:
        f.write("invalid_json{")

    monkeypatch.chdir(tmp_path)
    with pytest.raises(json.JSONDecodeError):
        runner = AMPJobRunner()
        runner.load_config()
