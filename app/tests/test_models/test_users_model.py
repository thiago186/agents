from app.views.users_schema import UserSchema
from app.models.users_model import usersCollection
from app.models.bcrypt_model import bcrypt_manager
from app.exceptions import DuplicateUserException, ModelInDbException

def test_save_user(_user):
    user_id = usersCollection.create_user(_user)

def test_save_duplicate_user(_user):

    try:
        usersCollection.create_user(_user)
        assert False, "Expected an error for saving a duplicate user"
    except Exception as e:
        assert isinstance(e, DuplicateUserException)

def test_save_invalid_user():
    invalid_user = {
        "_id" : "test_invalid_user",
        "email" : "test_invalid_user"
    }

    try:
        usersCollection.create_user(invalid_user)
        assert False, "Expected an error for saving an invalid user"
    except Exception as e:
        assert isinstance(e, ModelInDbException)

def test_retrieve_user(_user):
    user_id = _user.id
    user = usersCollection.retrieve_user_by_id(user_id)
    assert user
    assert user.id == user_id
    assert bcrypt_manager.check_password("test_password", user.hashed_password)

def test_update_user(_user):
    user_id = _user.id
    user = usersCollection.retrieve_user_by_id(user_id)
    user.first_name = "Updated First Name"
    result = usersCollection.update_user(user)
    assert result

def test_delete_user(_user):
    user_id = _user.id
    result = usersCollection.delete_document(user_id)
    assert result