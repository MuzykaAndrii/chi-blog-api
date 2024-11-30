from pydantic import BaseModel, ConfigDict, RootModel


class CreateRoleDTO(BaseModel):
    name: str


class PermissionReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class RoleReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class RoleWithPermsReadDTO(RoleReadDTO):
    permissions: list[PermissionReadDTO]


RolesWithPermsListReadDTO = RootModel[list[RoleReadDTO]]
RolesListReadDTO = RootModel[list[RoleReadDTO]]
