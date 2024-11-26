from flask import Blueprint, jsonify

from app.app import user_service
from app.users.exceptions import UserNotFound


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

    return jsonify(user)
