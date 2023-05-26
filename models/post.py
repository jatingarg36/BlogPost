import datetime
from typing import Optional, List

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, root_validator


class Tags(BaseModel):
    name: Optional[str]


# post model for creating a post
class PostModel(BaseModel):
    topic: Optional[str]
    content: Optional[str]
    tags: Optional[List[Tags]] = None

    @root_validator(pre=True)
    def validate_empty(cls, values):
        if "topic" not in values:
            raise ValueError('"topic" was not provided to the model')
        elif values.get("topic") == "":
            raise ValueError('empty topic was not provided to the model')
        if "content" not in values:
            raise ValueError('"content" was not provided to the model')
        elif values.get("content") == "":
            raise ValueError('empty content was not provided to the model')
        return values

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# Post Document to push/pull post to DB
class Post(Document, PostModel):
    author_id: Optional[PydanticObjectId]
    # slug: Optional[str]
    published: Optional[bool] = False
    published_at: Optional[datetime.datetime] = None

    created_at: Optional[datetime.datetime]
    modified_at: Optional[datetime.datetime]
