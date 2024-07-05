from app.views.users_schema import UserSchema
from app.models.bcrypt_model import bcrypt_manager


def test_user_schema(_user):
    assert _user.id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    assert bcrypt_manager.check_password("test_password", _user.hashed_password)
    assert not _user.password