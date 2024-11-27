from flask import Blueprint, jsonify

from app.app import articles_service
from app.articles.exceptions import ArticleNotFound
from app.utils.response import JsonResponse


router = Blueprint("articles", __name__, url_prefix="/articles")


@router.errorhandler(ArticleNotFound)
def handle_article_not_found(e: ArticleNotFound):
    return jsonify({"error": "AArticle not found"}), 404


@router.get("")
def get_all_articles():
    articles = articles_service.get_all_articles()

    return JsonResponse(articles.model_dump_json(), status=200)


@router.get("/<article_id:int>")
def get_article(article_id: int):
    article = articles_service.get_article_by_id(article_id)

    return JsonResponse(article.model_dump_json(), status=200)
