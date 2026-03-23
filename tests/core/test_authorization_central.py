from core.authorization_central import AuthorizationCentral


def test_authorization_central_init():
    auth_central = AuthorizationCentral()
    assert isinstance(auth_central, AuthorizationCentral)
