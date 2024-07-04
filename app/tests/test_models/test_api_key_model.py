"""This module contains the tests for the API key model"""
from app.models.api_keys_model import apiKeysCollection
from app.schemas.api_key_schema import APIKeySchema

def test_create_api_key(_api_key):
    """Testing the creation of an API key document in the database"""
    document_id = apiKeysCollection.create_api_key(_api_key)
    assert document_id is not None

def test_retrieve_organization_api_keys(_organization):
    """Testing the retrieval of all API key documents for an organization"""
    organization_id = _organization.id
    api_keys = apiKeysCollection.retrieve_organization_api_keys(organization_id)
    assert isinstance(api_keys, list)
    assert len(api_keys) > 0
    assert isinstance(api_keys[0], APIKeySchema)

def test_retrieve_user_api_keys(_user):
    """Testing the retrieval of all API key documents for a user"""
    user_id = _user.id
    api_keys = apiKeysCollection.retrieve_user_api_keys(user_id)
    assert isinstance(api_keys, list)
    assert len(api_keys) > 0
    assert isinstance(api_keys[0], APIKeySchema)

def test_retrieve_organization_api_key(_api_key_value, _organization):
    """Testing the retrieval of a specific API key for an organization"""
    organization_id = _organization.id
    api_key = apiKeysCollection.retrieve_organization_api_key(_api_key_value, organization_id)
    assert api_key is not None

def test_is_valid_api_key(_api_key_value, _organization):
    """Testing the validation of an API key for an organization"""
    is_valid = apiKeysCollection.is_valid_api_key(_api_key_value, _organization.id)
    assert is_valid is True


def test_revoke_api_key(_api_key_value, _organization):
    """Testing the revocation of an API key"""
    result = apiKeysCollection.revoke_api_key(_api_key_value, _organization.id)
    assert result is True

def test_delete_api_key(_api_key_value, _organization):
    """Testing the deletion of an API key"""
    result = apiKeysCollection.delete_api_key(_api_key_value, _organization.id)
    assert result
