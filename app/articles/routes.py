from flask import Blueprint

from app.app import articles_service
from app.utils.response import JsonResponse


router = Blueprint("articles", __name__, url_prefix="/articles")


@router.get("")
def get_all_articles():
    articles = articles_service.get_all_articles()

    return JsonResponse(articles.model_dump_json(), status=200)
