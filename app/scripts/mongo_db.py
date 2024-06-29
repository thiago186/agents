from pymongo import MongoClient
from config import settings

def create_collections():
    client = MongoClient(settings.mongo_uri)
    db = client[settings.mongo_db]
    db.create_collection('agents')
    db.create_collection('conversations')
    print("Collections created!")

if __name__ == "__main__":
    create_collections()