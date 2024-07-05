from pymongo import MongoClient

from app.config import settings
from app.logging_config import models_logger

class MongoCollection:
    def __init__(self, collection_name, db_name=settings.mongo_db, uri=settings.mongo_uri):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_document(self, document: dict):
        try:
            result = self.collection.insert_one(document)
            models_logger.debug(f"Document created with id: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            models_logger.error(f"Error creating document: {e}")
            raise e

    def retrieve_document_by_id(self, doc_id: str):
        try:
            document = self.collection.find_one({"_id": doc_id})
            return document
        except Exception as e:
            models_logger.error(f"Error retrieving document: {e}")

    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document in the collection by its id
        Args:
            doc_id (str): The id of the document to delete
        Returns:
            bool: True if the document was deleted, False otherwise
        """
        try:
            result = self.collection.delete_one({"_id": doc_id})
            models_logger.debug(f"Document deleted: {result.deleted_count}")
            return result.deleted_count > 0
        except Exception as e:
            models_logger.error(f"Error deleting document: {e}")
            raise e

    def edit_document_by_id(self, doc_id: str, new_document: dict) -> int:
        """Edit a document in the collection by its id
        Args:
            doc_id (str): The id of the document to edit
            new_document (dict): The new document data
        Returns:
            int: The number of documents modified
        """
        try:
            result = self.collection.replace_one({"_id": doc_id}, new_document)
            return result.modified_count > 0
        except Exception as e:
            models_logger.error(f"Error editing document: {e}")
            raise e

    def retrieve_documents_by_fields(self, query: dict):
        try:
            documents = self.collection.find(query)
            return list(documents)
        except Exception as e:
            models_logger.error(f"Error retrieving documents: {e}")
            raise e

agents_collection = MongoCollection("agents")
conversations_collection = MongoCollection("conversations")