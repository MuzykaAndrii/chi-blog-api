from flask import Blueprint, request
from flasgger import swag_from

from app.articles.swagger import docs
from app.app import rbac
from app.app import articles_service
from app.articles.permissions import user_is_article_owner
from app.users.dto import UserReadDTO
from app.utils.response import JsonResponse


router = Blueprint("articles", __name__)


@router.get("/articles")
@swag_from(docs.GET_ARTICLES_LIST)
def get_all_articles():
    search_query = request.args.get("query", None)

    if search_query:
        articles = articles_service.search_articles(search_query)
    else:
        articles = articles_service.get_all_articles()

    return JsonResponse(articles.model_dump_json(), status=200)


@router.get("/users/<int:user_id>/articles")
@swag_from(docs.GET_USER_ARTICLES)
def get_user_articles(user_id: int):
    articles = articles_service.get_user_articles(user_id)
    return JsonResponse(articles.model_dump_json(), status=200)


@router.get("/articles/<int:article_id>")
@swag_from(docs.GET_ARTICLE)
def get_article(article_id: int):
    article = articles_service.get_article_by_id(article_id)

    return JsonResponse(article.model_dump_json(), status=200)


@router.post("/articles")
@rbac.permission_required("articles.can_create")
@swag_from(docs.POST_ARTICLE)
def create_article(current_user: UserReadDTO):
    created_article = articles_service.create_article(current_user, request.get_json())
    return JsonResponse(created_article.model_dump_json(), status=201)


@router.delete("/articles/<int:article_id>")
@rbac.permission_required("articles.can_delete", unless=user_is_article_owner)
@swag_from(docs.DELETE_ARTICLE)
def delete_article(article_id: int):
    articles_service.delete_article(article_id)
    return JsonResponse(status=204)


@router.put("/articles/<int:article_id>")
@rbac.permission_required("articles.can_update", unless=user_is_article_owner)
@swag_from(docs.PUT_ARTICLE)
def update_article(article_id: int):
    updated_article = articles_service.update_article(article_id, request.get_json())
    return JsonResponse(updated_article.model_dump_json(), status=200)
