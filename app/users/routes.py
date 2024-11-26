from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.app import user_service
from app.users.exceptions import UserEmailAlreadyExists, UserNotFound
from app.utils.response import JsonResponse


router = Blueprint("users", __name__, url_prefix="/users")


@router.get("")
def get_users_list():
    users = user_service.get_all_users()
    return jsonify(users)


@router.get("/<int:user_id>")
def get_user(user_id: int):
    try:
        user = user_service.get_user_by_id(user_id)
    except UserNotFound:
        return jsonify({"error": "User not found"}), 404

    return JsonResponse(user.model_dump_json())


@router.post("")
def create_user():
    try:
        user = user_service.create(request.get_json())
        return JsonResponse(user.model_dump_json(), status=201)

    except ValidationError as e:
        return JsonResponse(e.json(), status=400)

    except UserEmailAlreadyExists:
        return jsonify({"error": "Email already exists"}), 400

    # TODO: handle username already exists error
