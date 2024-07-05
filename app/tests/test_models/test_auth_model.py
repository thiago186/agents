from app.models.auth_model import authHandler

def test_create_access_token(_user):
    token = authHandler.create_access_token_from_user(_user)
    assert token is not None

def test_decode_token(_jwt_token):
    payload = authHandler.decode_token(_jwt_token)
    assert payload is not None

def test_verify_token(_jwt_token):
    is_valid = authHandler.verify_token(_jwt_token)
    assert is_valid

def test_verify_token_invalid():
    token = "invalid_token"
    is_valid = authHandler.verify_token(token)
    assert not is_valid
