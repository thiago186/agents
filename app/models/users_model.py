"""This file contains the users model. It contains all the methods to interact with the users collection in the database"""

from datetime import datetime, timezone

from app.models.mongodb_model import MongoCollection
from app.logging_config import models_logger
from app.schemas.users_schema import UserSchema


class UsersCollection(MongoCollection):
    """Class to interact with users collection in the database"""

    def __init__(self):
        super().__init__("users")

    def create_user(self, user: UserSchema) -> str:
        """Create a new user in the database"""

        if not isinstance(user, UserSchema):
            raise ValueError("User must be an instance of UserSchema")

        if not user.hashed_password:
            user.hash_password()
        user_id = self.create_document(user.model_dump(by_alias=True))
        return user_id

    def retrieve_user_by_id(self, user_id: str) -> UserSchema:
        """Retrieve a user by its id"""

        document = self.retrieve_document_by_id(user_id)
        if document:
            return UserSchema(**document)

        raise ValueError(f"User with id {user_id} not found")
    
    def update_user(self, user: UserSchema) -> bool:
        """Update a user in the database"""

        if not isinstance(user, UserSchema):
            raise ValueError("User must be an instance of UserSchema")

        result = self.edit_document_by_id(user.id, user.model_dump(by_alias=True))
        return result


userCollection = UsersCollection()

if __name__ == "__main__":
    print("hello!")

