from pydantic import BaseModel, ConfigDict, EmailStr, Field, RootModel, model_validator

from app.users.pwd import PwdManagerMixin


class UserLoginDTO(BaseModel):
    """Data Transfer Object (DTO) for user login information."""

    email: EmailStr
    password: str


class UserReadDTO(BaseModel):
    """
    Data Transfer Object (DTO) for user read operations, returning basic user information.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr


UsersListReadDTO = RootModel[list[UserReadDTO]]


class UserCreateDTO(BaseModel, PwdManagerMixin):
    """
    Data Transfer Object (DTO) for creating a new user, with password validation.
    """

    username: str = Field(max_length=30, min_length=4)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)

    def model_dump(self, *args, **kwargs) -> dict:
        dumped = super().model_dump(*args, **kwargs, exclude=["password"])
        dumped["password_hash"] = self.gen_hash(self.password)
        return dumped
