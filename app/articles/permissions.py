from app.app import articles_service


def user_is_article_owner(current_user, *args, **kwargs) -> bool:
    article_id = kwargs.get("article_id", None)

    if not article_id:
        return False

    article = articles_service.get_article_by_id(article_id)

    return current_user.id == article.owner_id
