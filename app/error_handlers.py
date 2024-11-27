"""Common application-wide exception handlers"""

from flask import Flask, jsonify
from pydantic import ValidationError

from app.users.exceptions import UserNotFound
from app.utils.response import JsonResponse


def register_error_handlers(app: Flask):

    @app.errorhandler(UserNotFound)
    def handle_user_not_found(e: UserNotFound):
        return jsonify({"error": "User not found"}), 404

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return JsonResponse(e.json(), status=400)
