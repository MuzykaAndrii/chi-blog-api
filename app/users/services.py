from sqlalchemy.exc import IntegrityError

from app.users.pwd import PwdManagerMixin
from app.users.dao import UserDAO
from app.users.dto import UserCreateDTO, UserLoginDTO, UserReadDTO, UsersListReadDTO
from app.users.exceptions import (
    InvalidPassword,
    UserEmailAlreadyExists,
    UserNotFound,
    UsernameAlreadyExists,
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

    def get_all_users(self) -> UsersListReadDTO:
        users = self._dao.get_all()

        return UsersListReadDTO(users)

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
        validated_user_data = user_model.model_dump(exclude=["password"])
        validated_user_data["password_hash"] = self.gen_hash(user_model.password)

        try:
            user = self._dao.create(**validated_user_data)
        except IntegrityError:
            # TODO: add error handler for username already exists
            raise UserEmailAlreadyExists

        return UserReadDTO.model_validate(user)

    def update_user(self, user_id: int, user_data: dict) -> UserReadDTO:
        """Creates or updates a new user with provided registration data"""
        user = self._dao.get_one(user_id)

        if not user:
            raise UserNotFound

        user_model = UserCreateDTO(**user_data)
        validated_user_data = user_model.model_dump(exclude=["password"])
        validated_user_data["password_hash"] = self.gen_hash(user_model.password)

        try:
            updated_user = self._dao.update(user_id, **validated_user_data)
        except IntegrityError as e:
            constraint_name = (
                e.orig.diag.constraint_name if hasattr(e.orig, "diag") else None
            )

            if constraint_name == "uq_users_email":
                raise UserEmailAlreadyExists
            elif constraint_name == "uq_users_username":
                raise UsernameAlreadyExists
            else:
                raise e

        return UserReadDTO.model_validate(updated_user)
