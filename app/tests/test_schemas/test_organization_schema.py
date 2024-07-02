import pytest

from app.schemas.api_key_schema import APIKeySchema
from app.schemas.organization_schema import OrganizationSchema, OrganizationRoles

def test_organization_schema(_organization):
        
        print(f"organization: {_organization}")

        assert _organization.id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
        assert _organization.organization_name == "Test Organization"
        assert isinstance(_organization.api_keys[0], APIKeySchema)
        assert _organization.api_keys[0].id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
        assert _organization.api_keys[0].organization_id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
