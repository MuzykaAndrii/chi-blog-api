from flask import Blueprint, jsonify, request

from app.app import articles_service, auth_service
from app.articles.exceptions import ArticleNotFound
from app.users.dto import UserReadDTO
from app.utils.response import JsonResponse


router = Blueprint("articles", __name__, url_prefix="/articles")


@router.errorhandler(ArticleNotFound)
def handle_article_not_found(e: ArticleNotFound):
    return jsonify({"error": "AArticle not found"}), 404


@router.get("")
def get_all_articles():
    articles = articles_service.get_all_articles()

    return JsonResponse(articles.model_dump_json(), status=200)


@router.get("/<int:article_id>")
def get_article(article_id: int):
    article = articles_service.get_article_by_id(article_id)

    return JsonResponse(article.model_dump_json(), status=200)


@router.post("")
@auth_service.auth_required
def create_article(current_user: UserReadDTO):
    created_article = articles_service.create_article(current_user, request.get_json())
    return JsonResponse(created_article.model_dump_json(), status=201)
