from pydantic import BaseModel, ConfigDict, EmailStr, Field, RootModel, model_validator


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


class UserCreateDTO(BaseModel):
    """
    Data Transfer Object (DTO) for creating a new user, with password validation.
    """

    username: str = Field(max_length=30, min_length=4)
    email: EmailStr
    pwd1: str = Field(min_length=8, max_length=50)
    pwd2: str = Field(min_length=8, max_length=50)

    @model_validator(mode="before")
    def check_passwords_match(cls, values: dict):
        """Validates that the two password fields (pwd1 and pwd2) match."""

        pwd1, pwd2 = values.get("pwd1"), values.get("pwd2")

        if pwd1 != pwd2:
            raise ValueError("Passwords do not match")

        return values
