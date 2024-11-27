class AuthError(Exception):
    """Base class for authentication errors"""


class AuthenticationExpired(AuthError):
    """Error raised when authentication is expired"""


class NotAuthenticated(AuthError):
    """Error raised when the user is not authenticated"""
