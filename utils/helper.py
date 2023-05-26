import hashlib

from beanie import PydanticObjectId
from fastapi import HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from models.post import Post
from models.user import User
from utils.jwt_bearer import JWT_Bearer


# create a sha256 hash key for password
def hash_password(password: str) -> str:
    try:
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed
    except Exception as e:
        print("unable to hash password: ", e)
        raise HTTPException(500, "Internal Server Error")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        if hashed_password == hash_password(password):
            return True
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(500, "Internal Server Error")
    return False


# jwt bearer for fastapi_jet_auth
jwt_bearer = JWT_Bearer()


# Authenticate the user for protected routes
async def authorized_user(auth: AuthJWT = Depends(jwt_bearer)) -> User:
    try:
        auth.jwt_required()
        print("Validating User:", auth.get_jwt_subject())
    except Exception as e:
        print(e)
        raise HTTPException(401, "Unauthorized Access")

    user_id = auth.get_jwt_subject()
    print("UserID: ", user_id)
    user = await User.get(user_id)
    if user is None:
        raise HTTPException(400, "Bad Request")
    return user


# what if post is invalid,  can't comment right?
async def verify_post(post_id: PydanticObjectId = ""):
    post = await Post.get(post_id)
    if post is None:
        raise HTTPException(400, "Bad Request")
    return post


# query parameters dependency for large response routes
async def pagination(skip: int = 0, limit: int = 5) -> dict:
    return {"skip": skip, "limit": limit}
