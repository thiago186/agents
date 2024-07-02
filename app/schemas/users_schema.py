"""This file contains all users schemas for the application."""

from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum
import uuid

from pydantic import AliasChoices, BaseModel, Field, ConfigDict

class UserBaseSchema(BaseModel):
    """Base schema for a user. It doesn't contain hashed password field"""

    model_config = ConfigDict(use_enum_values=True)
    id: str = Field(
        default_factory=None,
        alias=AliasChoices("id", "_id", "id_"),
        serialization_alias="_id",
    )
    email: str
    username: str
    first_name: str
    password: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserInDbSchema(UserBaseSchema):
    """Schema for a user in the database"""

    hashed_password: str


if __name__ == "__main__":
    user = UserBaseSchema(
        id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        email="email@email.com",
        username="username",
        first_name="First Name",
        password="test_password"
    )

    print(user.model_dump())