"""This file contains all users schemas for the application."""

from datetime import datetime, timezone
from typing import Optional

from pydantic import AliasChoices, BaseModel, Field

from app.models.bcrypt_model import bcrypt_manager
from app.views.config_dict_schema import gen_config_dict

class UserBaseSchema(BaseModel):
    """Base schema for the user received at the login endpoint"""
    
    model_config = gen_config_dict

    email: str
    password: str


class UserSchema(BaseModel):
    """Base schema for a user. It doesn't contain hashed password field"""

    model_config = gen_config_dict
    id: str = Field(
        default_factory=None,
        alias=AliasChoices("id", "_id", "id_"),
        serialization_alias="_id",
    )
    email: str
    username: str
    first_name: str
    password: Optional[str] = Field(default=None, exclude=True)
    hashed_password: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __init__(self, **data):
        super().__init__(**data)
        if self.hashed_password is None and self.password is not None:
            self.hash_password()

    def hash_password(self):
        """Hash the password and set it to the hashed_password attribute"""
        self.hashed_password = bcrypt_manager.hash_password(self.password)
        self.password = None


if __name__ == "__main__":
    user = UserSchema(
        id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        email="email@email.com",
        username="username",
        first_name="First Name",
        password="test_password",
    )

    print(user.model_dump())
