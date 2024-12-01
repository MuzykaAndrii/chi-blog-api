from flask import Blueprint, jsonify, request
from flasgger import swag_from

from app.app import rbac
from app.app import role_service
from app.rbac.exceptions import PermissionNotFound, RoleAlreadyExists, RoleNotFound
from app.rbac.swagger.docs import role as role_docs
from app.utils.response import JsonResponse


router = Blueprint("roles", __name__, url_prefix="/roles")


@router.errorhandler(RoleNotFound)
def handle_role_not_found(e: RoleNotFound):
    return jsonify({"error": "role not found"}), 404


@router.get("")
@rbac.permission_required("roles.can_view")
@swag_from(role_docs.GET_ROLES)
def get_all_roles():
    """Get all roles with permissions included"""
    roles = role_service.get_all_roles()
    return JsonResponse(roles.model_dump_json(), status=200)


@router.get("/<int:role_id>")
@rbac.permission_required("roles.can_view")
@swag_from(role_docs.GET_ROLE)
def get_role(role_id: int):
    role = role_service.get_role_by_id(role_id)
    return JsonResponse(role.model_dump_json(), status=200)


@router.post("")
@rbac.permission_required("roles.can_create")
@swag_from(role_docs.CREATE_ROLE)
def create_role():
    try:
        role = role_service.create_role(request.get_json())
    except RoleAlreadyExists:
        return jsonify({"error": "Role already exists"}), 409

    return JsonResponse(role.model_dump_json(), status=201)


@router.put("/<int:role_id>")
@rbac.permission_required("roles.can_update")
@swag_from(role_docs.UPDATE_ROLE)
def update_role(role_id: int):
    try:
        role = role_service.update_role(role_id, request.get_json())
    except RoleAlreadyExists:
        return jsonify({"error": "Role name already exists"}), 409

    return JsonResponse(role.model_dump_json(), status=200)


@router.delete("/<int:role_id>")
@rbac.permission_required("roles.can_delete")
@swag_from(role_docs.DELETE_ROLE)
def delete_role(role_id: int):
    role_service.delete_role(role_id)
    return JsonResponse(status=204)


@router.get("/<int:role_id>/permissions")
@rbac.permission_required("roles.can_view")
@swag_from(role_docs.GET_ROLE_PERMISSIONS)
def get_role_permissions(role_id: int):
    permissions = role_service.get_role_permissions(role_id)
    return JsonResponse(permissions.model_dump_json(), status=200)


@router.post("/<int:role_id>/permissions/<int:permission_id>")
@rbac.permission_required("roles.can_assign_permissions")
@swag_from(role_docs.ASSIGN_PERMISSION_TO_ROLE)
def assign_permission_to_role(role_id: int, permission_id: int):
    try:
        new_permissions_list = role_service.assign_permission_to_role(
            role_id, permission_id
        )
        return JsonResponse(new_permissions_list.model_dump_json(), status=200)

    except PermissionNotFound:
        return jsonify({"error": "Permission not found"}), 404


@router.delete("/<int:role_id>/permissions/<int:permission_id>")
@rbac.permission_required("roles.can_remove_permissions")
@swag_from(role_docs.REMOVE_PERMISSION_FROM_ROLE)
def remove_permission_from_role(role_id: int, permission_id: int):
    try:
        new_permissions_list = role_service.remove_permission_from_role(
            role_id, permission_id
        )
        return JsonResponse(new_permissions_list.model_dump_json(), status=200)

    except PermissionNotFound:
        return jsonify({"error": "Permission not found"}), 404
