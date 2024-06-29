from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoCRUD:
    def __init__(self, db_name, collection_name, uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_document(self, document):
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def retrieve_document_by_id(self, doc_id):
        document = self.collection.find_one({"_id": ObjectId(doc_id)})
        return document

    def delete_document(self, doc_id):
        result = self.collection.delete_one({"_id": ObjectId(doc_id)})
        return result.deleted_count > 0

    def edit_document_by_id(self, doc_id, new_document):
        result = self.collection.replace_one({"_id": ObjectId(doc_id)}, new_document)
        return result.modified_count > 0

    def retrieve_documents_by_fields(self, query):
        documents = self.collection.find(query)
        return list(documents)

# Example usage
if __name__ == "__main__":
    db_name = "test_db"
    collection_name = "test_collection"

    mongo_crud = MongoCRUD(db_name, collection_name)

    # Create a document
    document = {"name": "John Doe", "age": 30, "email": "john.doe@example.com"}
    doc_id = mongo_crud.create_document(document)
    print(f"Document created with ID: {doc_id}")

    # Retrieve the document by ID
    retrieved_doc = mongo_crud.retrieve_document_by_id(doc_id)
    print("Retrieved Document:", retrieved_doc)

    # Edit the document by ID
    new_document = {"name": "Jane Doe", "age": 25, "email": "jane.doe@example.com"}
    is_edited = mongo_crud.edit_document_by_id(doc_id, new_document)
    print(f"Document edited: {is_edited}")

    # Retrieve the edited document by ID
    edited_doc = mongo_crud.retrieve_document_by_id(doc_id)
    print("Edited Document:", edited_doc)

    # Retrieve documents by any given field(s)
    query = {"name": "Jane Doe"}
    found_docs = mongo_crud.retrieve_documents_by_fields(query)
    print("Documents found with query:", found_docs)

    # Delete the document
    is_deleted = mongo_crud.delete_document(doc_id)
    print(f"Document deleted: {is_deleted}")