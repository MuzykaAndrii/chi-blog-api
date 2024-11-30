from typing import Protocol


class SupportsDefaultRoleIDAttr(Protocol):
    default_role_id: int
