"""This file contains the users model. It contains all the methods to interact with the users collection in the database"""

from datetime import datetime, timezone

import bcrypt

from app.schemas.users_schema import UserInDbSchema
from app.models.mongodb_model import MongoCollection




class UsersCollection(MongoCollection):
    """Class to interact with users collection in the database"""

    def __init__(self):
        super().__init__("users")


userCollection = UsersCollection()

if __name__ == "__main__":
    print('hello!')
    