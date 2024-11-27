from pydantic import BaseModel, ConfigDict, Field, RootModel
from datetime import datetime


class ArticleCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(max_length=255)
    body: str
    owner_id: int | None = None


class ArticleReadDTO(ArticleCreateDTO):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


ArticlesListReadDTO = RootModel[list[ArticleReadDTO]]
