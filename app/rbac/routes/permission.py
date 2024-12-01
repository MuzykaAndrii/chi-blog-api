from flask import Blueprint, jsonify, request
from flasgger import swag_from

from app.app import rbac
from app.rbac.exceptions import PermissionAlreadyExists, PermissionNotFound
from app.utils.response import JsonResponse
from app.app import permission_service
from app.rbac.swagger.docs import permission as perm_docs


router = Blueprint("permissions", __name__, url_prefix="/permissions")


@router.errorhandler(PermissionNotFound)
def handle_permission_not_found(e: PermissionNotFound):
    return jsonify({"error": "Permission not found"}), 404


@router.errorhandler(PermissionAlreadyExists)
def handle_permission_already_exists(e: PermissionAlreadyExists):
    return jsonify({"error": "Permission with specified name already exists"}), 409


@router.get("")
@rbac.permission_required("permissions.can_view")
@swag_from(perm_docs.GET_PERMISSIONS)
def get_all_permissions():
    permissions = permission_service.get_all_permissions()
    return JsonResponse(permissions.model_dump_json(), status=200)


@router.get("/<int:permission_id>")
@rbac.permission_required("permissions.can_view")
@swag_from(perm_docs.GET_PERMISSION)
def get_permission(permission_id: int):
    permission = permission_service.get_permission_by_id(permission_id)
    return JsonResponse(permission.model_dump_json(), status=200)


@router.post("")
@rbac.permission_required("permissions.can_create")
@swag_from(perm_docs.CREATE_PERMISSION)
def create_permission():
    permission = permission_service.create_permission(request.get_json())

    return JsonResponse(permission.model_dump_json(), status=201)


@router.put("/<int:permission_id>")
@rbac.permission_required("permissions.can_update")
@swag_from(perm_docs.UPDATE_PERMISSION)
def update_permission(permission_id: int):
    permission = permission_service.update_permission(permission_id, request.get_json())

    return JsonResponse(permission.model_dump_json(), status=200)


@router.delete("/<int:permission_id>")
@rbac.permission_required("permissions.can_delete")
@swag_from(perm_docs.DELETE_PERMISSION)
def delete_permission(permission_id: int):
    permission_service.delete_permission(permission_id)
    return JsonResponse(status=204)
