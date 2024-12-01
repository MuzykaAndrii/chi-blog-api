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
