from app.models.api_keys_model import apiKeysCollection
from app.schemas.api_key_schema import APIKeySchema, APIKeyRole, APIKeyStatus

def test_create_api_key(_api_key):
    """Testing the creation of an API key document in the database"""
    document_id = apiKeysCollection.create_api_key(_api_key)
    print(document_id)

def test_retrieve_api_key(_api_key):
    """
    Testing the retrieval of an API key document from the database
    This test simulates the situation where the user gives a key and the server needs to validate if the key is valid for the given organization
    """

    valid_api
