from sqlalchemy.exc import IntegrityError

from .pwd import PwdManagerMixin
from .dao import UserDAO
from .dto import UserCreateDTO, UserLoginDTO, UserReadDTO
from .exceptions import (
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

    def get_by_credentials(self, credentials: UserLoginDTO) -> UserReadDTO:
        """Authenticates a user using their login credentials."""

        user = self._dao.get_by_email(credentials.email)

        if not user:
            raise UserNotFound

        if not self.verify_hash(credentials.password, user.password_hash):
            raise InvalidPassword

        return UserReadDTO.model_validate(user)

    def create(self, user_data: UserCreateDTO) -> UserReadDTO:
        """Creates a new user with the provided registration data."""

        user_data_dict = user_data.model_dump(exclude=["pwd1", "pwd2"])
        user_data_dict["password_hash"] = self.gen_hash(user_data.pwd1)

        try:
            user = self._dao.create(**user_data_dict)
        except IntegrityError:
            # TODO: add error handler for username already exists
            raise UserEmailAlreadyExists

        return UserReadDTO.model_validate(user)
