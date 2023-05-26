import datetime

from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi_jwt_auth import AuthJWT

import utils.helper as _
from config import CONFIG
from models.user import User, UserModel, UserAuth

router = APIRouter(tags=["auth"])


# Signup Route
@router.post('/signup', summary="New User Signup")
async def add_user(new_user: UserModel):
    try:
        user = await User.find_one(User.email == new_user.email)

        if user is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User already exists")

        hash_password = _.hash_password(new_user.password)
        user = User(email=new_user.email, password=hash_password,
                    name=new_user.name,
                    created_at=datetime.datetime.now(),
                    modified_at=datetime.datetime.now())
        if user is None:
            raise HTTPException(500, "Internal Server Error")

        user = await user.create()
        if user is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error: Could not create user")
        content = {"msg": "User Created Successfully",
                   "user": str(user.id)}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")


# Login Route
@router.post('/login', summary="User Login")
async def login_user(user_creds: UserAuth, auth: AuthJWT = Depends()):
    try:
        user = await User.find_one({"email": str(user_creds.email)})
        if user is None or not _.verify_password(user_creds.password, user.password):
            raise HTTPException(401, "Bad Credentials")
        access_token = auth.create_access_token(subject=str(user.id),
                                                expires_time=datetime.timedelta(
                                                    minutes=CONFIG.AUTHJWT_ACCESS_TOKEN_EXPIRES))

        response = JSONResponse(status_code=status.HTTP_200_OK,
                                content={"msg": "Successfully Logged In",
                                         "user": str(user.id),
                                         "access_token": access_token})
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")
