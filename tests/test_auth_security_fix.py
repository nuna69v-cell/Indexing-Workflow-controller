import sys  # noqa: E402
from unittest.mock import MagicMock  # noqa: E402

# Mock third-party dependencies required for tests
for mod in ['backtrader', 'fastapi', 'fastapi.testclient', 'pydantic_settings', 'joblib', 'aiohttp', 'pandas', 'numpy']:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

import os  # noqa: E402
import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402

from fastapi import HTTPException  # noqa: E402

from api.utils.auth import get_current_user  # noqa: E402


class TestAuthLogic(unittest.TestCase):

    @patch.dict(os.environ, {"TESTING": "1"})
    def test_testing_mode_bypass(self):
        # When TESTING is set, missing credentials should return mock user
        user = get_current_user(credentials=None)
        self.assertEqual(user, {"username": "testuser", "exp": None})

    @patch.dict(os.environ, {}, clear=True)
    def test_production_mode_enforcement(self):
        # When TESTING is NOT set, missing credentials should raise 401
        with self.assertRaises(HTTPException) as cm:
            get_current_user(credentials=None)
        self.assertEqual(cm.exception.status_code, 401)

    @patch.dict(os.environ, {}, clear=True)
    @patch("api.utils.auth.jwt")
    @patch("api.utils.auth.settings")
    def test_production_mode_valid_token(self, mock_settings, mock_jwt):
        # When TESTING is NOT set, valid credentials should work
        mock_settings.SECRET_KEY = "secret"
        mock_settings.ALGORITHM = "HS256"

        mock_jwt.decode.return_value = {"sub": "realuser", "exp": 123456}

        credentials = MagicMock()
        credentials.credentials = "valid_token"

        user = get_current_user(credentials=credentials)
        self.assertEqual(user, {"username": "realuser", "exp": 123456})
        mock_jwt.decode.assert_called_once()


if __name__ == "__main__":
    unittest.main()
