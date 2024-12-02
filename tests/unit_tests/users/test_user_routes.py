from unittest.mock import MagicMock, patch

from flask.testing import FlaskClient
import pytest
from flask import Flask

from app.users.services import UserService


class MockRBAC:
    def permission_required(self, permission):
        def decorator(func):
            return func

        return decorator


@pytest.fixture
def app() -> Flask:
    """Create a Flask test app with user routes."""
    app = Flask(__name__)

    with patch("app.users.routes.user_service", MagicMock(UserService)):
        with patch("app.users.routes.rbac", MockRBAC()):
            from app.users.routes import router

            app.register_blueprint(router)

    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
