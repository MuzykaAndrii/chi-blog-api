from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.app import user_service
from app.users.exceptions import UserEmailAlreadyExists, UserNotFound
from app.utils.response import JsonResponse


router = Blueprint("users", __name__, url_prefix="/users")


@router.errorhandler(UserNotFound)
def handle_user_not_found_error(e):
    return jsonify({"error": "User not found"}), 404


@router.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    return JsonResponse(e.json(), status=400)


@router.get("")
def get_users_list():
    users = user_service.get_all_users()
    return JsonResponse(users.model_dump_json())


@router.get("/<int:user_id>")
def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id)

    return JsonResponse(user.model_dump_json())


@router.post("")
def create_user():
    try:
        user = user_service.create(request.get_json())
        return JsonResponse(user.model_dump_json(), status=201)

    except UserEmailAlreadyExists:
        return jsonify({"error": "Email already exists"}), 400

    # TODO: handle username already exists error


@router.put("/<int:user_id>")
def update_user(user_id: int):
    updated_user = user_service.update_user(user_id, request.get_json())
    return JsonResponse(updated_user.model_dump_json(), status=200)
