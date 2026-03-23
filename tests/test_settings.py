import os
from unittest.mock import patch
from config.settings import load_env

def test_load_env():
    with patch('config.settings.load_dotenv') as mock_load_dotenv:
        with patch.dict(os.environ, {'DB_URL': 'mock_db_url', 'API_KEY': 'mock_api_key'}, clear=True):
            result = load_env()

            mock_load_dotenv.assert_called_once()
            assert result == {
                'DB_URL': 'mock_db_url',
                'API_KEY': 'mock_api_key'
            }

def test_load_env_missing_vars():
    with patch('config.settings.load_dotenv') as mock_load_dotenv:
        with patch.dict(os.environ, {}, clear=True):
            result = load_env()

            mock_load_dotenv.assert_called_once()
            assert result == {
                'DB_URL': None,
                'API_KEY': None
            }
