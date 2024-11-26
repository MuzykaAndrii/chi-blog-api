from flask import Blueprint, jsonify

from app.app import user_service


router = Blueprint("users", __name__, url_prefix="/users")


@router.get("")
def get_users_list():
    users = user_service.get_all_users()
    return jsonify(users)
