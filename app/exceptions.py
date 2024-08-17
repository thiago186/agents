from pymongo.errors import DuplicateKeyError

class ModelInDbException(Exception):
    """Base class for exceptions in the models module."""
    pass

class ObjectNotFoundException(ModelInDbException):
    """Exception raised when an object is not found in the database"""
    pass

class DuplicateUserException(ModelInDbException):
    def __init__(self, duplicated_key, db_name):
        message = f"User with '{duplicated_key}' already exists in databse '{db_name}'"
        super().__init__(message)

class DuplicateOrganizationException(DuplicateKeyError):
    """General exception for when an organization already exists in the database"""
    pass