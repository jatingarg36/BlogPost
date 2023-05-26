from typing import Optional

from pydantic import BaseSettings


class Setting(BaseSettings):
    PORT: Optional[int] = 5000
    HOST: Optional[str] = 'localhost'

    DATABASE: Optional[str] = 'blog'
    DATABASE_URL: Optional[str] = 'mongodb://localhost:27017/?retryWrites=true&w=majority'

    AUTHJWT_SECRET_KEY: Optional[str]
    AUTHJWT_ACCESS_TOKEN_EXPIRES: Optional[int]
    AUTHJWT_ALGORITHM: Optional[str] = "HS256"

    class Config:
        env_file = '.env'
        orm_mode = True


CONFIG = Setting()
