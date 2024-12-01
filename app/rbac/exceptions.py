class RoleError(Exception):
    """Base exception for role errors"""


class RoleNotFound(RoleError):
    """Exception what occurred when role not found"""


class RoleAlreadyExists(RoleError):
    """Exception what occurred when role already exists"""


class PermissionNotFound(RoleError):
    """Exception when permission not found."""


class PermissionAlreadyExists(RoleError):
    """Exception when permission already exists"""
