import random

from faker import Faker

from app.app import user_service, articles_service, role_service, permission_service
from app.rbac.exceptions import PermissionAlreadyExists
from app.users.dto import UserReadDTO
from app.users.exceptions import UserEmailAlreadyExists, UsernameAlreadyExists

fake = Faker()


def create_mock_users(num_users) -> UserReadDTO:
    roles = ["admin", "editor", "viewer"]

    base_admin = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "password",
        "role_id": role_service._role_dao.get_by_name("admin").id,
    }
    try:
        user_service.create(base_admin)
    except (UserEmailAlreadyExists, UsernameAlreadyExists):
        print("Base admin found, creation skipped")
    else:
        print(
            f"Base admin created: email: '{base_admin['email']}' password: '{base_admin['password']}'"
        )

    users = []
    for _ in range(num_users):
        role = random.choice(roles)
        user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": "password",
            "role_id": role_service._role_dao.get_by_name(role).id,
        }
        user = user_service.create(user_data)
        print(f"User created: {user}")
        users.append(user)
    return users


def create_mock_articles(users: list[UserReadDTO]):
    for user in users:
        num_articles = random.randint(2, 5)
        for _ in range(num_articles):
            article_data = {
                "title": fake.sentence(),
                "body": fake.text(),
                "owner_id": user.id,
            }
            article = articles_service.create_article(user, article_data)
            print(f"Article created: '{article.title}'")


def assign_permissions():
    permissions = [
        # user entities
        "users.can_create",
        "users.can_read",
        "users.can_update",
        "users.can_delete",
        # article entities
        "articles.can_create",
        "articles.can_read",
        "articles.can_update",
        "articles.can_delete",
        # role entity
        "roles.can_view",
        "roles.can_create",
        "roles.can_read",
        "roles.can_update",
        "roles.can_delete",
        "roles.can_assign_permissions",
        "roles.can_remove_permissions",
        # permission entity
        "permissions.can_view",
        "permissions.can_create",
        "permissions.can_read",
        "permissions.can_update",
        "permissions.can_delete",
    ]

    for permission in permissions:
        try:
            p = permission_service.create_permission({"name": permission})
        except PermissionAlreadyExists:
            print(f"Permission '{permission}' already exists, creation skipped")
        else:
            print(f"Permission created: {p}")

    admin_role = role_service._role_dao.get_by_name("admin")
    for permission in permissions:
        perm = permission_service._permission_dao.get_by_name(permission)
        role_service.assign_permission_to_role(admin_role.id, perm.id)
        print(f"Permission {permission} assigned to admin role")

    editor_role = role_service._role_dao.get_by_name("editor")
    editor_perm = permission_service._permission_dao.get_by_name("articles.can_update")
    role_service.assign_permission_to_role(editor_role.id, editor_perm.id)
    print(f"Permission {editor_perm.name} assigned to editor role")


if __name__ == "__main__":
    role_service.create_base_roles_if_not_exists()
    mock_users = create_mock_users(random.randint(10, 15))
    create_mock_articles(mock_users)
    assign_permissions()
