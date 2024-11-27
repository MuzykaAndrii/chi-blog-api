from flask import request, Blueprint

from app.app import auth_service
from app.utils.response import JsonResponse
from app.users.exceptions import InvalidPassword

router = Blueprint("auth", __name__, url_prefix="/auth")


@router.post("/login")
def login():
    """Logs in a user and returns auth token if credentials are valid."""

    try:
        return auth_service.login_user(request.get_json())

    except InvalidPassword:
        return JsonResponse({"error": "Invalid password"}, status=401)
