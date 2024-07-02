"""This module contains the API key schema for the applicaiton"""

from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum
from uuid import uuid4

from pydantic import AliasChoices, BaseModel, Field, ConfigDict


class APIKeyRole(str, Enum):
    """Supported roles for API keys"""

    admin = "admin"

class APIKeyStatus(str, Enum):
    """Supported statuses for API keys"""

    active = "active"
    revoked = "revoked"

class APIKeySchema(BaseModel):
    """Schema for an API key in the database"""

    model_config = ConfigDict(use_enum_values=True)
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        alias=AliasChoices("id", "_id", "id_"),
        serialization_alias="_id",
    )
    key_status: APIKeyStatus = APIKeyStatus.active.value
    key_hash: str
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
    
    role: APIKeyRole = APIKeyRole.admin.value
    key_status: APIKeyStatus = APIKeyStatus.active.value

    created_by: str
    organization_id: str

    def get_api_key(self):
        """Get the API Key"""
        #TODO: Implement the logic to generate the API key
        key_dict = self.model_dump()
        key_dict["key_hash"] = "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
        key_dict["final_chars"] = "fc4e7"
        api_key = "temp_api_key"
        return APIKeySchema(**key_dict), api_key
        
    

if __name__ == "__main__":
    new_api_key = NewAPIKeySchema(
        created_by="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        organization_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        role=APIKeyRole.admin
    )

    print(new_api_key.model_dump())
    api_key_schema, api_key = new_api_key.get_api_key()