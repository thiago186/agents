class ModelInDbException(Exception):
    """Base class for exceptions in the models module."""
    pass

class DuplicateUserException(ModelInDbException):
    def __init__(self, duplicated_key, db_name):
        message = f"User with '{duplicated_key}' already exists in databse '{db_name}'"
        super().__init__(message)
