from unittest.mock import patch
from amp_auth import AMPAuth


class TestAMPAuthAuthenticate:
    def setup_method(self):
        self.auth = AMPAuth()

    @patch.object(AMPAuth, "parse_token")
    @patch.object(AMPAuth, "_validate")
    def test_authenticate_success(self, mock_validate, mock_parse_token):
        """Test successful authentication when parse_token and _validate both succeed."""
        mock_parse_token.return_value = {"user_id": "123", "session_hash": "abc"}
        mock_validate.return_value = True

        result = self.auth.authenticate("valid_token")

        assert result is True
        mock_parse_token.assert_called_once_with("valid_token")
        mock_validate.assert_called_once_with({"user_id": "123", "session_hash": "abc"})

    @patch.object(AMPAuth, "parse_token")
    @patch.object(AMPAuth, "_validate")
    def test_authenticate_invalid_token(self, mock_validate, mock_parse_token):
        """Test authentication failure when _validate returns False."""
        mock_parse_token.return_value = {}  # E.g. when token format is invalid
        mock_validate.return_value = False

        result = self.auth.authenticate("invalid_token")

        assert result is False
        mock_parse_token.assert_called_once_with("invalid_token")
        mock_validate.assert_called_once_with({})

    @patch.object(AMPAuth, "parse_token")
    def test_authenticate_exception(self, mock_parse_token):
        """Test authentication catches and handles exceptions gracefully."""
        # Force parse_token to raise an Exception
        mock_parse_token.side_effect = Exception("Unexpected error during parsing")

        result = self.auth.authenticate("error_token")

        # The except block should catch the Exception and return False
        assert result is False
        mock_parse_token.assert_called_once_with("error_token")
