from flask import Blueprint

from app.utils.response import JsonResponse
from app.app import permission_service


router = Blueprint("permissions", __name__, url_prefix="/permissions")


@router.get("")
def get_all_permissions():
    permissions = permission_service.get_all_permissions()
    return JsonResponse(permissions.model_dump_json(), status=200)


@router.get("/<int:permission_id>")
def get_permission(permission_id: int):
    permission = permission_service.get_permission_by_id(permission_id)
    return JsonResponse(permission.model_dump_json(), status=200)
