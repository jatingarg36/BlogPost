from beanie import PydanticObjectId
from fastapi import HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

import utils.helper as _
from models.user import User

router = APIRouter(dependencies=[Depends(_.authorized_user)])


# Get all user, with user authentication
@router.get("/all")
async def get_users(page: dict = Depends(_.pagination)):
    try:
        users = await User.aggregate([{'$skip': page['skip'] * page['limit']}, {'$limit': page['limit']}],
                                     projection_model=User).to_list()
        if users is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No user found")
        response = JSONResponse(status_code=status.HTTP_200_OK,
                                content={"users": jsonable_encoder(users)})
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")


# Get one user, with user authentication
@router.get('/{user_id}')
async def get_user(user_id: PydanticObjectId):
    try:
        user = await User.get(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No such user found")
        response = JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")
