from unittest.mock import patch

import amp_auth


def test_get_user_info_delegates_to_amp_auth():
    """Test get_user_info delegates to the global amp_auth instance."""
    with patch("amp_auth.amp_auth.get_user_info") as mock_get_user_info:
        mock_get_user_info.return_value = {
            "user_id": "test_user",
            "session_hash": "test_hash",
            "authenticated": True,
        }

        result = amp_auth.get_user_info()

        assert result == {
            "user_id": "test_user",
            "session_hash": "test_hash",
            "authenticated": True,
        }
        mock_get_user_info.assert_called_once()


def test_get_user_info_unauthenticated():
    """Test get_user_info when the user is not authenticated."""
    with patch("amp_auth.amp_auth.get_user_info") as mock_get_user_info:
        mock_get_user_info.return_value = {
            "authenticated": False,
        }

        result = amp_auth.get_user_info()

        assert result == {
            "authenticated": False,
        }
        mock_get_user_info.assert_called_once()
