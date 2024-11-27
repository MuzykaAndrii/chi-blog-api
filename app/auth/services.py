from functools import wraps
from typing import Callable

from flask import request, jsonify

from bookstore.auth.jwt import AuthTokenManager
from bookstore.users.services import UserService
from bookstore.users.dto import UserCreateDTO, UserLoginDTO, UserReadDTO
from bookstore.response import JsonResponse
from bookstore.auth.exceptions import AuthError


class AuthService:
    """Provides user authentication services"""

    cookie_name: str = "auth_token"

    def __init__(
        self, token_handler: AuthTokenManager, user_service: UserService
    ) -> None:
        self._token_handler = token_handler
        self._user_service = user_service

    def register_user(self, credentials: UserCreateDTO) -> UserReadDTO:
        """Registers a new user and returns user data."""

        return self._user_service.create(credentials)

    def login_user(self, credentials: UserLoginDTO) -> JsonResponse:
        """Authenticates a user and returns a response with an auth token cookie."""

        user = self._user_service.get_by_credentials(credentials)
        token = self._token_handler.create_token(user.id)

        resp = jsonify({"token": token})
        resp.set_cookie(self.cookie_name, token)

        return resp, 200

    def auth_required(self, router: Callable):
        """Decorator to protect routes, requiring a valid auth token to access."""

        @wraps(router)
        def wrapper(*args, **kwargs):
            token = request.cookies.get(self.cookie_name)

            try:
                self._token_handler.read_token(token)
            except AuthError:
                return JsonResponse(status=401)
            else:
                return router(*args, **kwargs)

        return wrapper
