from flask import request
from pydantic import ValidationError

from bookstore.app import app, auth_service
from bookstore.users.dto import UserCreateDTO, UserLoginDTO
from bookstore.response import JsonResponse
from bookstore.users.exceptions import (
    InvalidPassword,
    UserEmailAlreadyExists,
    UserNotFound,
)


@app.route("/register", methods=["POST"])
def register():
    """Registers a new user with the provided credentials."""

    try:
        user_create_data = UserCreateDTO(**request.json)
        auth_service.register_user(user_create_data)
        return JsonResponse(status=201)

    except ValidationError as e:
        return JsonResponse(e.json(), status=400)

    except UserEmailAlreadyExists:
        return JsonResponse({"error": "Email already in use"}, status=400)


@app.route("/login", methods=["POST"])
def login():
    """Logs in a user and returns an auth token if credentials are valid."""

    try:
        login_data = UserLoginDTO(**request.json)
        return auth_service.login_user(login_data)

    except ValidationError as e:
        return JsonResponse(e.json(), status=400)

    except UserNotFound:
        return JsonResponse({"error": "User not found"}, status=404)

    except InvalidPassword:
        return JsonResponse({"error": "Invalid password"}, status=401)
