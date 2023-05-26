from typing import Optional

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import ValidationError

from config import CONFIG
from database.db import initiate_database
from routers import user, auth, post

app = FastAPI()

# Adding routes for individual task
app.include_router(auth.router, prefix='/auth', tags=["auth"])
app.include_router(user.router, prefix='/user', tags=["users"])
app.include_router(post.router, prefix='/post', tags=["post"])


@AuthJWT.load_config
def get_config():
    return CONFIG


# Adding event at startup for connecting to DB
@app.on_event("startup")
async def start_database():
    try:
        await initiate_database()
        print("Database Successfully Initialised")
    except Exception as e:
        print("Error occurred while connecting to Database: ", e)


@app.exception_handler(ValidationError)
def validation_exception_handle(req: Request, exc: ValidationError):
    return JSONResponse(status_code=int(exc.status_code), content={"detail": exc.message})


@app.exception_handler(AuthJWTException)
def jwt_exception_handler(req: Request, exc: AuthJWTException):
    return JSONResponse(status_code=int(exc.status_code), content={"detail": exc.message})


@app.get("/")
async def index(name: Optional[str] = None):
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"msg": f'Welcome {name.upper() + " " if name is not None else ""}to BlogPost API'})
