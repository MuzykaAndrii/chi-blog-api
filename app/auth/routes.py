from flask import request, Blueprint
from flasgger import swag_from

from app.app import auth_service
from app.utils.response import JsonResponse
from app.users.exceptions import InvalidPassword
from app.auth.swagger import docs

router = Blueprint("auth", __name__, url_prefix="/auth")


@router.post("/login")
@swag_from(docs.LOGIN_USER)
def login():
    """Logs in a user and returns auth token if credentials are valid."""

    try:
        return auth_service.login_user(request.get_json())

    except InvalidPassword:
        return JsonResponse({"error": "Invalid password"}, status=401)
