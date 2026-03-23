import pytest
from amp_auth import AMPAuth, logout_user, amp_auth


@pytest.fixture
def auth_instance(tmp_path):
    auth = AMPAuth()
    # Use a temporary file for auth_file so we don't mess with real data
    auth.auth_file = tmp_path / "test_amp_auth.json"
    return auth


def test_logout_with_existing_file(auth_instance, capsys):
    # Setup
    auth_instance.auth_file.write_text('{"test": "data"}')
    auth_instance.session_token = "test_token"
    auth_instance.user_id = "user123"
    auth_instance.session_hash = "hash123"
    auth_instance.is_logged_in = True
    auth_instance.current_user = "user123"

    assert auth_instance.auth_file.exists()

    # Act
    auth_instance.logout()

    # Assert
    assert not auth_instance.auth_file.exists()
    assert auth_instance.session_token is None
    assert auth_instance.user_id is None
    assert auth_instance.session_hash is None
    assert auth_instance.is_logged_in is False
    assert auth_instance.current_user is None

    # Check printed output
    captured = capsys.readouterr()
    assert "✅ Logged out successfully" in captured.out


def test_logout_without_existing_file(auth_instance, capsys):
    # Setup
    auth_instance.session_token = "test_token"
    auth_instance.user_id = "user123"
    auth_instance.session_hash = "hash123"
    auth_instance.is_logged_in = True
    auth_instance.current_user = "user123"

    assert not auth_instance.auth_file.exists()

    # Act
    auth_instance.logout()

    # Assert
    assert not auth_instance.auth_file.exists()
    assert auth_instance.session_token is None
    assert auth_instance.user_id is None
    assert auth_instance.session_hash is None
    assert auth_instance.is_logged_in is False
    assert auth_instance.current_user is None

    # Check printed output
    captured = capsys.readouterr()
    assert "✅ Logged out successfully" in captured.out


def test_global_logout_user(monkeypatch):
    # Setup
    logout_called = False

    def mock_logout():
        nonlocal logout_called
        logout_called = True

    monkeypatch.setattr(amp_auth, "logout", mock_logout)

    # Act
    logout_user()

    # Assert
    assert logout_called is True
