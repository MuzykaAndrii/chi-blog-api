from flask import Blueprint, jsonify, request

from app.app import role_service
from app.rbac.exceptions import RoleAlreadyExists, RoleNotFound
from app.utils.response import JsonResponse


router = Blueprint("roles", __name__, url_prefix="/roles")


@router.errorhandler(RoleNotFound)
def handle_role_not_found(e: RoleNotFound):
    return jsonify({"error": "role not found"}), 404


@router.get("")
def get_all_roles():
    """Get all roles with permissions included"""
    roles = role_service.get_all_roles()
    return JsonResponse(roles.model_dump_json(exclude_none=True), status=200)


@router.get("/<int:role_id>")
def get_role(role_id: int):
    role = role_service.get_role_by_id(role_id)
    return JsonResponse(role.model_dump_json(), status=200)


@router.post("")
def create_role():
    try:
        role = role_service.create_role(request.get_json())
    except RoleAlreadyExists:
        return jsonify({"error": "Role already exists"}), 409

    return JsonResponse(role.model_dump_json(), status=201)


@router.put("/<int:role_id>")
def update_role(role_id: int):
    try:
        role = role_service.update_role(role_id, request.get_json())
    except RoleAlreadyExists:
        return jsonify({"error": "Role name already exists"}), 409

    return JsonResponse(role.model_dump_json(), status=200)
