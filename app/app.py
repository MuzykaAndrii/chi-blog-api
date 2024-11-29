from datetime import timedelta

from flask import Flask

from app.articles.dao import ArticleDAO
from app.articles.services import ArticleService
from app.auth.config import AuthSettings
from app.auth.jwt import JwtManager
from app.auth.services import AuthService
from app.db.config import DbSettings
from app.config import ENV_FILE_PATH
from app.db.database import Database
from app.rbac.services import AuthorizationService, RoleService
from app.rbac.dao import RoleDAO
from app.users.dao import UserDAO
from app.users.services import UserService


db_settings = DbSettings(_env_file=ENV_FILE_PATH)
db = Database(db_settings)

users_dao = UserDAO(db.session_factory)
user_service = UserService(users_dao)

articles_dao = ArticleDAO(db.session_factory)
articles_service = ArticleService(articles_dao)

auth_settings = AuthSettings(_env_file=ENV_FILE_PATH)
auth_jwt_manager = JwtManager("HS256", auth_settings.AUTH_SECRET, timedelta(days=1))
auth_service = AuthService(auth_jwt_manager, user_service)

permission_service = AuthorizationService(auth_service, user_service)

role_dao = RoleDAO(db.session_factory)
role_service = RoleService(
    role_dao=role_dao,
    base_roles={"viewer", "editor", "admin"},
    default_role="viewer",
)


def create_app():
    app = Flask(__name__)
    from app.users.routes import router as users_router
    from app.auth.routes import router as auth_router
    from app.articles.routes import router as articles_router

    app.register_blueprint(users_router)
    app.register_blueprint(auth_router)
    app.register_blueprint(articles_router)

    from app.error_handlers import register_error_handlers

    register_error_handlers(app)

    return app
