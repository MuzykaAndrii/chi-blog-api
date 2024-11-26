from flask import Flask

from app.db.config import DbSettings
from app.config import ENV_FILE_PATH
from app.db.database import Database
from app.users.dao import UserDAO
from app.users.services import UserService


db_settings = DbSettings(_env_file=ENV_FILE_PATH)
db = Database(db_settings)

users_dao = UserDAO(db.session_factory)
user_service = UserService(users_dao)


def create_app():
    app = Flask(__name__)
    from app.users.routes import router as users_router

    app.register_blueprint(users_router)

    return app
