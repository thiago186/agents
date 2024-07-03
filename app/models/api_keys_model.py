from app.models.mongodb_model import MongoCollection
from app.models.api_hash_model import apiHashManager
from app.schemas.api_key_schema import APIKeySchema, APIKeyStatus
from app.logging_config import models_logger
from app.exceptions import ModelInDbException


class APIKeysCollection(MongoCollection):
    """Class to interact with api_keys collection in the database"""
    
    def __init__(self):
        super().__init__("api_keys")

    def create_api_key(self, api_key: APIKeySchema) -> str:
        """
        Create a new api_key in the database
        """
        try:
            if not isinstance(api_key, APIKeySchema):
                raise ValueError("APIKey must be an instance of APIKeySchema")
            
            if not api_key.hashed_key:
                raise

            api_key_id = self.create_document(api_key.model_dump(by_alias=True))
            return api_key_id

        except Exception as e:
            models_logger.error(e)
            raise e
        
    def retrieve_api_key(self, key: str) -> APIKeySchema:
        """Retrieve an api_key by its key"""
        
        try:
            hashed_key = apiHashManager.hash_api_key(key)
            document = self.retrieve_documents_by_fields({"hashed_key": hashed_key})
            if document:
                return APIKeySchema(**document)
            
        except Exception as e:
            models_logger.warning(e)
            raise e
        
    def revoke_api_key(self, key: str) -> bool:
        """Revoke an api_key from the database"""
            
        try:
            api_key = self.retrieve_api_key(key)
            if api_key:
                api_key.key_status = APIKeyStatus.revoked.value
                result = self.update_document(api_key)
                return result
            
            raise ModelInDbException("Could not find the API key provided to revoke")
        
        except Exception as e:
            models_logger.error(e)
            raise e
        
    def delete_api_key(self, key: str) -> bool:
        """Delete an api_key from the database"""
            
        try:
            result = self.delete_document(key)
            return result
        except Exception as e:
            models_logger.error(e)
            raise e
        
apiKeysCollection = APIKeysCollection()