import json
import os


def test_basic_imports():
    assert True


def test_environment_variables():
    os.environ["TEST_VAR"] = "test_value"
    assert os.environ.get("TEST_VAR") == "test_value"


def test_json_parsing():
    test_data = {"key": "value", "number": 42}
    json_str = json.dumps(test_data)
    parsed_data = json.loads(json_str)
    assert parsed_data == test_data
