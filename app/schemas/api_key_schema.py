"""This module contains the API key schema for the applicaiton"""

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import AliasChoices, BaseModel, Field

from app.schemas.config_dict_schema import gen_config_dict
from app.models.api_hash_model import apiHashManager
from app.models.bcrypt_model import bcrypt_manager


class APIKeyRole(str, Enum):
    """Supported roles for API keys"""

    admin = "admin"


class APIKeyStatus(str, Enum):
    """Supported statuses for API keys"""

    active = "active"
    revoked = "revoked"


class APIKeySchema(BaseModel):
    """Schema for an API key in the database"""

    model_config = gen_config_dict
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        alias=AliasChoices("id", "_id", "id_"),
        serialization_alias="_id",
    )
    hashed_key: str
    key_status: APIKeyStatus = APIKeyStatus.active.value
    role: APIKeyRole
    organization_id: str
    final_chars: str
    created_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __init__(self, **data):
        super().__init__(**data)

    def is_key_active(self):
        """Get the status of the API key"""
        return self.key_status == APIKeyStatus.active.value


class NewAPIKeySchema(BaseModel):
    """Schema for creating a new API key"""

    model_config = gen_config_dict

    role: APIKeyRole = APIKeyRole.admin.value
    key_status: APIKeyStatus = APIKeyStatus.active.value

    created_by: str
    organization_id: str

    def get_api_key(self):
        """Get the API Key"""
        api_key = apiHashManager.generate_api_key()
        key_dict = self.model_dump()
        key_dict["hashed_key"] = bcrypt_manager.hash_password(api_key)
        key_dict["final_chars"] = api_key[-4:]
        return APIKeySchema(**key_dict), api_key


if __name__ == "__main__":
    new_api_key = NewAPIKeySchema(
        created_by="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        organization_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        role=APIKeyRole.admin,
    )

    print(new_api_key.model_dump())
    api_key_schema, api_key = new_api_key.get_api_key()
