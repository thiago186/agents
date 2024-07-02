from datetime import datetime
import pytest

from ...schemas.api_key_schema import APIKeySchema, APIKeyRole, APIKeyStatus

def test_api_key_schema(_api_key):
    
        assert _api_key.id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
        assert _api_key.organization_id == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
        assert _api_key.hashed_key == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
        assert _api_key.role == APIKeyRole.admin.value
        assert _api_key.key_status == APIKeyStatus.active.value
        assert _api_key.created_by == "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
        assert _api_key.final_chars == "fc4e7"
        assert _api_key.created_at == datetime(2000, 1, 1)