from typing import Protocol


class SupportsIdentity(Protocol):
    id: int


class SupportsGetCurrentUser(Protocol):
    def get_current_user(self) -> SupportsIdentity | None: ...


class SupportsPermissionCheck(Protocol):
    def user_has_permission(self, user_id: int, permission: str) -> bool: ...
