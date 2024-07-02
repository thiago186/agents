from app.schemas.users_schema import UserSchema
from app.models.users_model import userCollection
from app.models.bcrypt_model import bcrypt_manager

def test_save_user(_user):
    user_id = userCollection.create_user(_user)

def test_retrieve_user(_user):
    user_id = _user.id
    user = userCollection.retrieve_user_by_id(user_id)
    assert user
    assert user.id == user_id
    assert bcrypt_manager.check_password("test_password", user.hashed_password)

def test_update_user(_user):
    user_id = _user.id
    user = userCollection.retrieve_user_by_id(user_id)
    user.first_name = "Updated First Name"
    result = userCollection.update_user(user)
    assert result

def test_delete_user(_user):
    user_id = _user.id
    result = userCollection.delete_document(user_id)
    assert result