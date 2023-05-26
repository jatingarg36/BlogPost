import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, root_validator
from pydantic.networks import EmailStr


# used for login and authentication purpose
class UserAuth(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]

    @root_validator(pre=True)
    def validate_empty(cls, values):
        if "email" not in values:
            raise ValueError('"email" was not provided to the model')
        elif values.get("email") == "":
            raise ValueError('empty email was not provided to the model')
        if "password" not in values:
            raise ValueError('"password" was not provided to the model')
        elif values.get("password") == "":
            raise ValueError('empty password was not provided to the model')
        return values

    class Config:
        orm_mode = True


# extended to help signup with name and created time
class UserModel(UserAuth):
    name: Optional[str]
    created_at: Optional[datetime.datetime] = datetime.datetime.now()


# User Document to push/pull user data in DB.
class User(Document, UserModel):
    modified_at: Optional[datetime.datetime]

    def __str__(self):
        return f"id: {self.id} Email: {self.email} Name: {self.name}"

