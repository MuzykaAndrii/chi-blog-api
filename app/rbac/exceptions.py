class RoleError(Exception):
    """Base exception for role errors"""


class RoleNotFound(RoleError):
    """Exception what occurred when role not found"""
