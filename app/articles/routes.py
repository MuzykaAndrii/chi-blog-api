from flask import Blueprint, jsonify, request

from app.app import rbac
from app.app import articles_service, auth_service
from app.articles.exceptions import ArticleNotFound
from app.articles.permissions import user_is_article_owner
from app.users.dto import UserReadDTO
from app.utils.response import JsonResponse


router = Blueprint("articles", __name__)


@router.errorhandler(ArticleNotFound)
def handle_article_not_found(e: ArticleNotFound):
    return jsonify({"error": "Article not found"}), 404


@router.get("/articles")
def get_all_articles():
    search_query = request.args.get("query", None)

    if search_query:
        articles = articles_service.search_articles(search_query)
    else:
        articles = articles_service.get_all_articles()

    return JsonResponse(articles.model_dump_json(), status=200)


@router.get("/users/<int:user_id>/articles")
def get_user_articles(user_id: int):
    articles = articles_service.get_user_articles(user_id)
    return JsonResponse(articles.model_dump_json(), status=200)


@router.get("/articles/<int:article_id>")
def get_article(article_id: int):
    article = articles_service.get_article_by_id(article_id)

    return JsonResponse(article.model_dump_json(), status=200)


@router.post("/articles")
@rbac.permission_required("articles.can_create")
def create_article(current_user: UserReadDTO):
    created_article = articles_service.create_article(current_user, request.get_json())
    return JsonResponse(created_article.model_dump_json(), status=201)


@router.delete("/articles/<int:article_id>")
@rbac.permission_required("articles.can_delete", unless=user_is_article_owner)
def delete_article(article_id: int):
    articles_service.delete_article(article_id)
    return JsonResponse(status=204)


@router.put("/articles/<int:article_id>")
@rbac.permission_required("articles.can_update", unless=user_is_article_owner)
def update_article(article_id: int):
    updated_article = articles_service.update_article(article_id, request.get_json())
    return JsonResponse(updated_article.model_dump_json(), status=200)
