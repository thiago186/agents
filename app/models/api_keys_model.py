from typing import List

from app.models.mongodb_model import MongoCollection
from app.models.api_hash_model import apiHashManager
from app.views.api_key_schema import APIKeySchema, APIKeyStatus
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

    def retrieve_organization_api_keys(
        self, organization_id: str, only_active_keys: bool = False
    ) -> List[APIKeySchema]:
        """Retrieve all api_keys for an organization"""

        try:
            query = {"organization_id": organization_id}
            if only_active_keys:
                query["key_status"] = APIKeyStatus.active.value
            api_keys = self.retrieve_documents_by_fields(query)
            return [APIKeySchema(**api_key) for api_key in api_keys]

        except Exception as e:
            models_logger.error(e)
            raise e

    def retrieve_user_api_keys(
        self, user_id: str, only_active_keys: bool = False
    ) -> List[APIKeySchema]:
        """
        Retrieve all api_keys for a user

        Args:
            user_id (str): The user id
            only_active_keys (bool, optional): If True, only active keys will be retrieved. Defaults to False.
        """

        try:
            query = {"created_by": user_id}
            if only_active_keys:
                query["key_status"] = APIKeyStatus.active.value

            api_keys = self.retrieve_documents_by_fields(query)
            api_keys = [APIKeySchema(**api_key) for api_key in api_keys]
            return api_keys
        except Exception as e:
            models_logger.error(e)
            raise e

    def retrieve_organization_api_key(
        self, key: str, organization_id: str
    ) -> APIKeySchema:
        """Retrieve a given api_key for an organizaton"""

        try:
            api_keys = self.retrieve_organization_api_keys(organization_id)
            for api_key in api_keys:
                if apiHashManager.check_api_hash(key, api_key.hashed_key):
                    return api_key
        except Exception:
            return None
        
    def is_valid_api_key(self, key: str, organization_id: str) -> bool:
        """Check if an api_key is valid and active for an given organization"""

        try:
            api_keys = self.retrieve_organization_api_keys(
                organization_id, only_active_keys=True
            )
            is_valid = any(
                [
                    apiHashManager.check_api_hash(key, api_key.hashed_key)
                    for api_key in api_keys
                ]
            )
            return is_valid
        except Exception as e:
            models_logger.error(e)
            raise e

    def revoke_api_key(self, key: str, organization_id: str) -> bool:
        """Revoke an api_key from the database"""

        try:
            api_key = self.retrieve_organization_api_key(key, organization_id)
            if api_key:
                api_key.key_status = APIKeyStatus.revoked.value
                result = self.update_document_by_id(api_key.id, api_key.model_dump(by_alias=True))
                return result

            raise ModelInDbException("Could not find the API key provided to revoke")

        except Exception as e:
            models_logger.error(e)
            raise e

    def delete_api_key(self, key: str, organization_id: str) -> bool:
        """Delete an api_key from the database"""

        try:
            api_key = self.retrieve_organization_api_key(key, organization_id)
            if api_key:
                result = self.delete_document(api_key.id)
                return result

            raise ModelInDbException("Could not find the API key provided to delete")
            
        except Exception as e:
            models_logger.error(e)
            raise e


apiKeysCollection = APIKeysCollection()
