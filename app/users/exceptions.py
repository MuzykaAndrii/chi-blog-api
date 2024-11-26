class UserError(Exception):
    """Base class for user errors"""


class UserNotFound(UserError):
    """Error raised when user is not found"""


class InvalidPassword(UserError):
    """Error raised when password is invalid"""


class UserEmailAlreadyExists(UserError):
    """Error raised when user email is already exists"""
