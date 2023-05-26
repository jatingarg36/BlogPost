import datetime
from typing import Union

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

import utils.helper as _
from models.post import Post, PostModel
from models.user import User
from routers import comment

router = APIRouter(dependencies=[Depends(_.authorized_user)])


# Fetch all post with user authentication
# Or Fetch all posts of one user
@router.get('/all', description="Get posts of users OR one user")
async def get_posts(user_id: Union[PydanticObjectId, None] = None, page: dict = Depends(_.pagination)):
    try:

        if user_id is None:
            posts = await Post.aggregate([{'$skip': page['skip'] * page['limit']}, {'$limit': page['limit']}],
                                         projection_model=Post).to_list()
        else:
            posts = await Post.aggregate(
                [{'$match': {'author_id': ObjectId(user_id)}}, {'$skip': page['skip'] * page['limit']},
                 {'$limit': page['limit']}],
                projection_model=Post).to_list()

        if posts is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No posts found")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"users": jsonable_encoder(posts)})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")


# Create Post Route, with user authentication
@router.post("/", description="Posting a blog")
async def create_post(content: PostModel, user: User = Depends(_.authorized_user)):
    try:
        post = Post(**content.__dict__, author_id=user.id,
                    created_at=datetime.datetime.now(),
                    modified_at=datetime.datetime.now())
        post = await post.create()
        if post is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error: Could not create post")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"users": jsonable_encoder(post)})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")


# Fetch one post, with user authentication
@router.get('/{post_id}', description="Get a post with Id")
async def get_post(post_id: PydanticObjectId):
    try:
        post = await Post.get(post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No post found")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"users": jsonable_encoder(post)})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")


# sub-route for comment, based on individual post
router.include_router(comment.router, prefix='/{post_id}/comment', tags=["comment"])
