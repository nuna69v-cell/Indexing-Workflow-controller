from amp_auth import AMPAuth

def test_parse_token_valid_no_prefix():
    auth = AMPAuth()
    result = auth.parse_token("12345_abcde12345")
    assert result == {
        "user_id": "12345",
        "session_hash": "abcde12345",
        "full_token": "sgamp_user_12345_abcde12345",
    }

def test_parse_token_valid_with_prefix():
    auth = AMPAuth()
    result = auth.parse_token("sgamp_user_9876_xyz123")
    assert result == {
        "user_id": "9876",
        "session_hash": "xyz123",
        "full_token": "sgamp_user_9876_xyz123",
    }

def test_parse_token_invalid_format_no_underscore():
    auth = AMPAuth()
    result = auth.parse_token("invalidtoken")
    assert result == {}

def test_parse_token_empty_string():
    auth = AMPAuth()
    result = auth.parse_token("")
    assert result == {}

def test_parse_token_error_handling_none():
    auth = AMPAuth()
    # Passing None will cause an AttributeError on .startswith,
    # which is caught by the except block.
    result = auth.parse_token(None)
    assert result == {}

def test_parse_token_error_handling_integer():
    auth = AMPAuth()
    # Passing an integer will cause an AttributeError on .startswith.
    result = auth.parse_token(12345)
    assert result == {}

def test_parse_token_error_handling_list():
    auth = AMPAuth()
    result = auth.parse_token(["user", "hash"])
    assert result == {}
