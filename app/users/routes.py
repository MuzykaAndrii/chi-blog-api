from flask import Blueprint, Response, jsonify, request
from flasgger import swag_from

from app.app import user_service, rbac
from app.users.exceptions import UserEmailAlreadyExists, UsernameAlreadyExists
from app.base.response import DtoResponse
from app.users.swagger import docs

router = Blueprint("users", __name__, url_prefix="/users")


@router.errorhandler(UserEmailAlreadyExists)
def handle_user_email_exists(e: UserEmailAlreadyExists):
    return jsonify({"error": "Email already exists"}), 400


@router.errorhandler(UsernameAlreadyExists)
def handle_username_exists(e: UsernameAlreadyExists):
    return jsonify({"error": "Username already exists"}), 400


@router.get("")
@swag_from(docs.GET_USERS_LIST)
def get_users_list():
    search_query = request.args.get("name", None)

    if search_query:
        users = user_service.search_users_by_name(search_query)
    else:
        users = user_service.get_all_users()

    return DtoResponse(users)


@router.get("/<int:user_id>")
@swag_from(docs.GET_USER)
def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id)
    return DtoResponse(user)


@router.post("")
@rbac.permission_required("users.can_create")
@swag_from(docs.CREATE_USER)
def create_user():
    user = user_service.create(request.get_json())
    return DtoResponse(user, status=201)


@router.put("/<int:user_id>")
@rbac.permission_required("users.can_update")
@swag_from(docs.UPDATE_USER)
def update_user(user_id: int):
    updated_user = user_service.update_user(user_id, request.get_json())
    return DtoResponse(updated_user, status=200)


@router.delete("/<int:user_id>")
@rbac.permission_required("users.can_delete")
@swag_from(docs.DELETE_USER)
def delete_user(user_id: int):
    user_service.delete_user(user_id)
    return Response(status=204)
