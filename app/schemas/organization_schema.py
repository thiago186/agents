"""This module contains the schemas for an organization"""

from datetime import datetime, timezone
from typing import List
from enum import Enum

from pydantic import AliasChoices, BaseModel, Field

from app.schemas.api_key_schema import APIKeySchema
from app.schemas.config_dict_schema import gen_config_dict

class OrganizationRoles(str, Enum):
    """ 
    Supported roles for oganizations'members:

    admin: Users with full access to managing al organization's resources, add/remove members.
    manager: Users with access to editing organization's agents and conversations. Not allowed to add/remove members.
    user: Users with access only to use agent's and start conversations via the API. Not allowed to change organization's resources.
    """

    admin = "admin"
    manager = "manager"
    user = "user"


class OrganizationSchema(BaseModel):
    """Schema for a organization in the database."""

    model_config = gen_config_dict
    id: str = Field(
        default_factory=None,
        alias=AliasChoices("id", "_id", "id_"),
        serialization_alias="_id",
    )
    organization_name: str
    owner_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    members: List[str] = []
    api_keys: List[APIKeySchema] = []

if __name__ == "__main__":
    organization = OrganizationSchema(
        id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        organization_name="Test Organization",
        owner_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        members=["e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"]
    )
    print(organization.model_dump())