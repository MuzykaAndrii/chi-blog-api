from typing import Any, Protocol


class SupportsIdProtocol(Protocol):
    id: int


class UserServiceProtocol(Protocol):

    def get_by_credentials(self, credentials: Any) -> SupportsIdProtocol: ...

    def get_user_by_id(self, id: int) -> SupportsIdProtocol: ...
