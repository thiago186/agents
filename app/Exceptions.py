class UsersModelException(Exception):
    """Base class for exceptions in the models module."""
    pass

class DuplicateUserException(UsersModelException):
    def __init__(self, message="User with this email already exists"):
        super().__init__(message)
