import struct
import json
from datetime import datetime
from api.services.ea_communication import MessageProtocol

def test_encode_message_basic():
    """Test that encode_message properly formats a message."""
    message_type = "SIGNAL"
    data = {"action": "BUY", "instrument": "EURUSD"}

    encoded = MessageProtocol.encode_message(message_type, data)

    # Check length prefix
    assert len(encoded) >= 4
    length = struct.unpack("!I", encoded[:4])[0]
    assert len(encoded) == 4 + length

    # Decode payload
    payload_str = encoded[4:].decode("utf-8")
    payload = json.loads(payload_str)

    # Verify payload content
    assert payload["type"] == message_type
    assert payload["data"] == data
    assert "timestamp" in payload
    # Verify timestamp format
    datetime.fromisoformat(payload["timestamp"])

def test_encode_message_empty_data():
    """Test encoding with empty data dictionary."""
    encoded = MessageProtocol.encode_message("HEARTBEAT", {})

    length = struct.unpack("!I", encoded[:4])[0]
    payload = json.loads(encoded[4:].decode("utf-8"))

    assert payload["type"] == "HEARTBEAT"
    assert payload["data"] == {}

def test_decode_message_valid():
    """Test decoding a valid message."""
    message_type = "RESPONSE"
    data = {"status": "OK"}
    encoded = MessageProtocol.encode_message(message_type, data)

    decoded = MessageProtocol.decode_message(encoded)
    assert decoded is not None
    assert decoded["type"] == message_type
    assert decoded["data"] == data

def test_decode_message_incomplete():
    """Test decoding an incomplete message."""
    # Less than 4 bytes
    assert MessageProtocol.decode_message(b"\x00\x00\x00") is None

    # Valid prefix but incomplete payload
    encoded = MessageProtocol.encode_message("TEST", {"key": "val"})
    assert MessageProtocol.decode_message(encoded[:-1]) is None

def test_decode_message_invalid_json():
    """Test decoding invalid JSON payload."""
    invalid_json = b"{invalid: json}"
    length_prefix = struct.pack("!I", len(invalid_json))
    encoded = length_prefix + invalid_json

    assert MessageProtocol.decode_message(encoded) is None

def test_decode_message_invalid_utf8():
    """Test decoding invalid UTF-8 payload."""
    invalid_utf8 = b"\xff\xfe\xfd"
    length_prefix = struct.pack("!I", len(invalid_utf8))
    encoded = length_prefix + invalid_utf8

    assert MessageProtocol.decode_message(encoded) is None
