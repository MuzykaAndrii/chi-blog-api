from pydantic import BaseModel, ConfigDict, Field, RootModel


class PermissionReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class RoleReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    permissions: list[PermissionReadDTO]


RolesListReadDTO = RootModel[list[RoleReadDTO]]
