import sys  # noqa: E402
from unittest.mock import MagicMock  # noqa: E402

# Mock third-party dependencies required for tests
for mod in ['backtrader', 'fastapi', 'fastapi.testclient', 'pydantic_settings', 'joblib', 'aiohttp', 'pandas', 'numpy']:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

import pytest  # noqa: E402
from cryptography.fernet import Fernet  # noqa: E402

import api.config  # noqa: E402
from utils.encryption import EncryptionManager  # noqa: E402


def test_key_generation_and_init():
    key = Fernet.generate_key().decode()
    manager = EncryptionManager(key=key)
    assert manager.cipher_suite is not None


def test_encryption_decryption_round_trip():
    key = Fernet.generate_key().decode()
    manager = EncryptionManager(key=key)

    original_text = "Secret Data 123!"
    encrypted = manager.encrypt(original_text)

    assert encrypted != original_text
    assert manager.decrypt(encrypted) == original_text


def test_empty_string():
    key = Fernet.generate_key().decode()
    manager = EncryptionManager(key=key)

    assert manager.encrypt("") == ""
    assert manager.decrypt("") == ""


def test_missing_key():
    # Save original key
    original_key = api.config.settings.CRYPTION_KEY
    # Force settings to None
    api.config.settings.CRYPTION_KEY = None

    try:
        manager = EncryptionManager(key=None)
        with pytest.raises(ValueError, match="Encryption key is not configured"):
            manager.encrypt("data")
    finally:
        # Restore original key
        api.config.settings.CRYPTION_KEY = original_key


def test_invalid_key_format():
    # Fernet keys must be 32 url-safe base64-encoded bytes.
    # Passing a random string should fail initialization (silently print error in __init__)
    # and leave cipher_suite as None.

    manager = EncryptionManager(key="invalid_key_short")
    assert manager.cipher_suite is None

    with pytest.raises(ValueError, match="Encryption key is not configured"):
        manager.encrypt("data")
