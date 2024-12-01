GET_ARTICLES_LIST = {
    "tags": ["Articles"],
    "description": "Get a list of all articles, optionally filtered by a search query.",
    "parameters": [
        {
            "name": "query",
            "in": "query",
            "description": "Search query to filter articles by title or body",
            "required": False,
            "schema": {"type": "string", "example": "Python"},
        }
    ],
    "responses": {
        "200": {
            "description": "List of articles",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "Article 1",
                            "owner_id": 1,
                            "created_at": "2024-12-01T00:00:00Z",
                        },
                        {
                            "id": 2,
                            "title": "Article 2",
                            "owner_id": 2,
                            "created_at": "2024-12-01T00:00:00Z",
                        },
                    ]
                }
            },
        },
        "400": {"description": "Invalid search query"},
    },
}

GET_USER_ARTICLES = {
    "tags": ["Articles"],
    "description": "Get a list of articles written by a specific user.",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "description": "ID of the user to get articles for",
            "required": True,
            "schema": {"type": "integer", "example": 1},
        }
    ],
    "responses": {
        "200": {
            "description": "List of articles by the user",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "User's Article",
                            "owner_id": 1,
                            "created_at": "2024-12-01T00:00:00Z",
                        }
                    ]
                }
            },
        },
        "404": {"description": "User not found"},
    },
}

GET_ARTICLE = {
    "tags": ["Articles"],
    "description": "Get details of a specific article by its ID.",
    "parameters": [
        {
            "name": "article_id",
            "in": "path",
            "description": "ID of the article to retrieve",
            "required": True,
            "schema": {"type": "integer", "example": 1},
        }
    ],
    "responses": {
        "200": {
            "description": "Article details",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Article 1",
                        "body": "Content of the article",
                        "owner_id": 1,
                        "created_at": "2024-12-01T00:00:00Z",
                    }
                }
            },
        },
        "404": {"description": "Article not found"},
    },
}

POST_ARTICLE = {
    "tags": ["Articles"],
    "description": "Create a new article.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "description": "The article data to create",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "example": "New Article"},
                    "body": {"type": "string", "example": "Content of the new article"},
                },
                "required": ["title", "body"],
            },
        }
    ],
    "responses": {
        "201": {
            "description": "Article successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 3,
                        "title": "New Article",
                        "body": "Content of the new article",
                        "owner_id": 1,
                        "created_at": "2024-12-01T00:00:00Z",
                    }
                }
            },
        },
        "400": {"description": "Invalid article data"},
    },
}

DELETE_ARTICLE = {
    "tags": ["Articles"],
    "description": "Delete an article by its ID.",
    "parameters": [
        {
            "name": "article_id",
            "in": "path",
            "description": "ID of the article to delete",
            "required": True,
            "schema": {"type": "integer", "example": 1},
        }
    ],
    "responses": {
        "204": {"description": "Article successfully deleted"},
        "404": {"description": "Article not found"},
    },
}

PUT_ARTICLE = {
    "tags": ["Articles"],
    "description": "Update an existing article by its ID.",
    "parameters": [
        {
            "name": "article_id",
            "in": "path",
            "description": "ID of the article to update",
            "required": True,
            "schema": {"type": "integer", "example": 1},
        },
        {
            "name": "body",
            "in": "body",
            "description": "Updated article data",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "example": "Updated Article Title"},
                    "body": {
                        "type": "string",
                        "example": "Updated content of the article",
                    },
                },
                "required": ["title", "body"],
            },
        },
    ],
    "responses": {
        "200": {
            "description": "Article successfully updated",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Updated Article Title",
                        "body": "Updated content of the article",
                        "owner_id": 1,
                        "created_at": "2024-12-01T00:00:00Z",
                    }
                }
            },
        },
        "404": {"description": "Article not found"},
        "400": {"description": "Invalid article data"},
    },
}
