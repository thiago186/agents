"""This file contains the users model. It contains all the methods to interact with the users collection in the database"""

from app.models.mongodb_model import MongoCollection
from app.logging_config import models_logger
from app.views.users_schema import UserSchema
from app.exceptions import DuplicateUserException, ModelInDbException


class UsersCollection(MongoCollection):
    """Class to interact with users collection in the database"""

    def __init__(self):
        super().__init__("users")

    def create_user(self, user: UserSchema) -> str:
        """
        Create a new user in the database
        Performs users duplicity validations
        To be created, the user must have a hashed password, a valid and unique email
        """
        try:
            if not isinstance(user, UserSchema):
                raise ModelInDbException("User must be an instance of UserSchema")

            # check for email field in user
            if not user.email:
                raise ModelInDbException("User must have an email")

            # check for duplicate email
            user_by_email = self.retrieve_documents_by_fields({"email": user.email})
            if user_by_email:
                raise DuplicateUserException("email", self.collection.name)

            if not user.hashed_password and user.password:
                user.hash_password()

            user_id = self.create_document(user.model_dump(by_alias=True))
            return user_id

        except Exception as e:
            models_logger.error(e)
            raise e

    def retrieve_user_by_id(self, user_id: str) -> UserSchema:
        """Retrieve a user by its id"""
        try:
            document = self.retrieve_document_by_id(user_id)
            if document:
                return UserSchema(**document)
            
        except Exception as e:
            models_logger.warning(e)
            raise e

    def retrieve_user_by_email(self, email: str) -> UserSchema:
        """Retrieve a user by its email"""
        try:
            document = self.retrieve_documents_by_fields({"email": email})
            if document:
                return UserSchema(**document[0])
            
        except Exception as e:
            models_logger.warning(e)
            raise e


    def update_user(self, user: UserSchema) -> str:
        """Update a user in the database"""

        try:
            if not isinstance(user, UserSchema):
                raise ValueError("User must be an instance of UserSchema")

            result = self.update_document_by_id(user.id, user.model_dump(by_alias=True))
            return result

        except Exception as e:
            models_logger.error(e)
            raise e


usersCollection = UsersCollection()

if __name__ == "__main__":
    user = UserSchema(
        id="user1",
        email="thiago.wander22@gmail.com",
        username="thiago.wander",
        first_name="Thiago",
        password="test_password"
    )

    usersCollection.create_user(user)