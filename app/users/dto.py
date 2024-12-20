from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    RootModel,
    field_validator,
)

from app.users.exceptions import InvalidPassword
from app.users.pwd import PwdManagerMixin


class UserLoginDTO(BaseModel, PwdManagerMixin):
    """Data Transfer Object (DTO) for user login information."""

    email: EmailStr
    password: str

    def verify_pwd(self, pwd_hash: bytes) -> None:
        if not self.verify_hash(self.password, pwd_hash):
            raise InvalidPassword


class UserReadDTO(BaseModel):
    """
    Data Transfer Object (DTO) for user read operations, returning basic user information.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: str

    @field_validator("role", mode="before")
    @classmethod
    def assign_role_name(cls, v):
        if isinstance(v, str):
            return v

        return v.name


UsersListReadDTO = RootModel[list[UserReadDTO]]


class UserCreateDTO(BaseModel, PwdManagerMixin):
    """
    Data Transfer Object (DTO) for creating a new user, with password validation.
    """

    username: str = Field(max_length=30, min_length=4)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
    role_id: int | None = None

    def model_dump(self, *args, **kwargs) -> dict:
        dumped = super().model_dump(*args, **kwargs, exclude=["password"])
        dumped["password_hash"] = self.gen_hash(self.password)
        return dumped
