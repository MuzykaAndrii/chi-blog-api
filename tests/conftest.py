import functools
from flask import Flask
from flask.testing import FlaskClient
import pytest


@pytest.fixture
def test_app() -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(test_app: Flask) -> FlaskClient:
    return test_app.test_client()


@pytest.fixture
def mock_rbac():
    class MockRBAC:
        def permission_required(self, permission, unless=None):
            def decorator(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    return func(*args, **kwargs)

                return wrapper

            return decorator

    return MockRBAC
