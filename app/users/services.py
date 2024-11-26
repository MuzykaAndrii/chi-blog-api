from sqlalchemy.exc import IntegrityError
from pydantic import TypeAdapter

from app.users.pwd import PwdManagerMixin
from app.users.dao import UserDAO
from app.users.dto import UserCreateDTO, UserLoginDTO, UserReadDTO
from app.users.exceptions import (
    InvalidPassword,
    UserEmailAlreadyExists,
    UserNotFound,
)


class UserService(PwdManagerMixin):
    """
    Service class for handling user-related operations.
    Extends PwdManagerMixin to leverage password hashing and verification methods.
    """

    def __init__(self, user_dao: UserDAO) -> None:
        self._dao = user_dao

    def get_user_by_id(self, user_id: int) -> UserReadDTO:
        user = self._dao.get_one(user_id)

        if not user:
            raise UserNotFound

        return UserReadDTO.model_validate(user)

    def get_all_users(self) -> list[UserReadDTO]:
        users = self._dao.get_all()

        users_list_adapter = TypeAdapter(list[UserReadDTO])

        # return [UserReadDTO(user) for user in users]
        return users_list_adapter.validate_python(users)

    def get_by_credentials(self, credentials: UserLoginDTO) -> UserReadDTO:
        """Authenticates a user using their login credentials."""

        user = self._dao.get_by_email(credentials.email)

        if not user:
            raise UserNotFound

        if not self.verify_hash(credentials.password, user.password_hash):
            raise InvalidPassword

        return UserReadDTO.model_validate(user)

    def create(self, user_data: dict) -> UserReadDTO:
        """Creates a new user with the provided registration data."""

        user_model = UserCreateDTO(**user_data)
        validated_user_data = user_model.model_dump(exclude=["pwd1", "pwd2"])
        validated_user_data["password_hash"] = self.gen_hash(user_model.pwd1)

        try:
            user = self._dao.create(**validated_user_data)
        except IntegrityError:
            # TODO: add error handler for username already exists
            raise UserEmailAlreadyExists

        return UserReadDTO.model_validate(user)
