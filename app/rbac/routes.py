from flask import Blueprint, request

from app.app import role_service
from app.utils.response import JsonResponse


router = Blueprint("roles", __name__, url_prefix="/roles")


@router.get("")
def get_all_roles():
    """Get all roles with permissions included"""
    roles = role_service.get_all_roles()
    return JsonResponse(roles.model_dump_json(exclude_none=True), status=200)


@router.get("/<int:role_id>")
def get_role(role_id: int):
    role = role_service.get_role_by_id(role_id)
    return JsonResponse(role.model_dump_json(), status=200)
