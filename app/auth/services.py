from functools import wraps
from typing import Callable

from flask import request, jsonify, Response

from app.auth.jwt import JwtManager
from app.auth.exceptions import AuthError
from app.auth.protocols import UserServiceProtocol


class AuthService:
    """Provides user authentication services"""

    cookie_name: str = "auth_token"

    def __init__(
        self,
        jwt_manager: JwtManager,
        user_service: UserServiceProtocol,
    ) -> None:
        self._jwt_manager = jwt_manager
        self._user_service = user_service

    def login_user(self, credentials: dict) -> Response:
        """Authenticates a user and returns a response with an auth token cookie."""

        user = self._user_service.get_by_credentials(credentials)
        token = self._jwt_manager.create_token(user.id)

        resp = jsonify({"token": token})
        resp.set_cookie(self.cookie_name, token)

        return resp

    def auth_required(self, router: Callable):
        """Decorator to protect routes, requiring a valid auth token to access."""

        @wraps(router)
        def wrapper(*args, **kwargs):
            token = request.cookies.get(self.cookie_name)

            try:
                self._jwt_manager.read_token(token)
            except AuthError:
                return jsonify(status=401)
            else:
                return router(*args, **kwargs)

        return wrapper
