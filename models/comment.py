import datetime
from typing import Optional

from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, root_validator


# comment model to create a comment
class CommentModel(BaseModel):
    comment: str

    @root_validator(pre=True)
    def validate_empty(cls, values):
        if "comment" not in values:
            raise ValueError('"comment" was not provided to the model')
        elif values.get("comment") == "":
            raise ValueError('empty comment was not provided to the model')
        return values

    class Config:
        orm_mode = True


# Comment Document to publish comment
# based on user_id and post_id
class Comment(Document, CommentModel):
    post_id: Optional[PydanticObjectId]
    comment_by: Optional[PydanticObjectId]
    created_at: Optional[datetime.datetime]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
