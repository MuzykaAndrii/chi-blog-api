from sqlalchemy.exc import IntegrityError

from app.users.dao import UserDAO
from app.users.dto import UserCreateDTO, UserLoginDTO, UserReadDTO, UsersListReadDTO
from app.users.exceptions import (
    UserEmailAlreadyExists,
    UserNotFound,
    UsernameAlreadyExists,
)
from app.users.protocols import SupportsDefaultRoleIDAttr


class UserService:
    """Service class for handling user-related operations."""

    def __init__(
        self,
        user_dao: UserDAO,
        default_role_id_getter: SupportsDefaultRoleIDAttr,
    ) -> None:
        self._dao = user_dao
        self.roles = default_role_id_getter

    def get_user_by_id(self, user_id: int) -> UserReadDTO:
        user = self._get_user_or_raise(user_id)
        return UserReadDTO.model_validate(user)

    def search_users_by_name(self, name: str) -> UsersListReadDTO:
        found_users = self._dao.search_by_name(name)
        return UsersListReadDTO(found_users)

    def get_all_users(self) -> UsersListReadDTO:
        users = self._dao.get_all()
        return UsersListReadDTO(users)

    def get_by_credentials(self, credentials: dict) -> UserReadDTO:
        """Authenticates a user using their login credentials."""
        validated_creds = UserLoginDTO(**credentials)
        user = self._dao.get_by_email(validated_creds.email)

        if not user:
            raise UserNotFound

        validated_creds.verify_pwd(user.password_hash)
        return UserReadDTO.model_validate(user)

    def create(self, user_data: dict) -> UserReadDTO:
        """Creates a new user with the provided registration data."""
        validated_user = UserCreateDTO(**user_data)

        if not validated_user.role_id:
            validated_user.role_id = self.roles.default_role_id

        try:
            user = self._dao.create(**validated_user.model_dump())
        except IntegrityError as e:
            self._catch_user_constraints_violation(e)

        return UserReadDTO.model_validate(user)

    def update_user(self, user_id: int, user_data: dict) -> UserReadDTO:
        """Updates user with provided update data."""
        self._get_user_or_raise(user_id)  # Ensure user exists before update

        validated_user = UserCreateDTO(**user_data)

        if not validated_user.role_id:
            validated_user.role_id = self.roles.default_role_id

        try:
            updated_user = self._dao.update(user_id, **validated_user.model_dump())
        except IntegrityError as e:
            self._catch_user_constraints_violation(e)

        return UserReadDTO.model_validate(updated_user)

    def delete_user(self, user_id: int) -> None:
        self._get_user_or_raise(user_id)
        self._dao.delete(user_id)

    def user_has_permission(self, user_id: int, permission: str) -> bool:
        """Check if a user has a specific permission through their role."""
        user = self._dao.get_with_permissions(user_id)

        if not user:
            raise UserNotFound

        return permission in {perm.name for perm in user.role.permissions}

    def _get_user_or_raise(self, user_id: int):
        user = self._dao.get_one(user_id)
        if not user:
            raise UserNotFound
        return user

    def _catch_user_constraints_violation(self, error: IntegrityError) -> None:
        """
        Inspects the IntegrityError to identify constraint violations and raises appropriate exceptions.
        """
        error_msg = str(error.orig)
        if "users_email_key" in error_msg:
            raise UserEmailAlreadyExists
        elif "users_username_key" in error_msg:
            raise UsernameAlreadyExists
        else:
            raise error
