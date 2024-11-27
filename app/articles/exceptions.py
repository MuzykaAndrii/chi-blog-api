class ArticleError(Exception):
    """Base class for article errors"""


class ArticleNotFound(ArticleError):
    """error raised whe the article does not exist"""
