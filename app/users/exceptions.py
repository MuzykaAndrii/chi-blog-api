from pydantic import ValidationError


class UserError(Exception):
    """Base class for user errors"""


class BookCreationError(UserError):
    """Error raised when creating a new user throws validation error"""

    def __init__(self, validation_error: ValidationError, **args):
        super().__init__(*args)
        self.validation_error = validation_error

    def json(self):
        return self.validation_error.json()


class UserNotFound(UserError):
    """Error raised when user is not found"""


class InvalidPassword(UserError):
    """Error raised when password is invalid"""


class UserEmailAlreadyExists(UserError):
    """Error raised when user email is already exists"""


class UsernameAlreadyExists(UserError):
    """Error raised when username is already exists"""
