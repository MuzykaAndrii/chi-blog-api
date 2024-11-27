from typing import Any, Protocol


class SupportsIdProtocol(Protocol):
    id: int


class UserServiceProtocol(Protocol):

    def get_by_credentials(self, credentials: Any) -> SupportsIdProtocol: ...
