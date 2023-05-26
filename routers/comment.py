import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.comment import Comment, CommentModel
from models.user import User
from utils import helper as _

router = APIRouter(dependencies=[Depends(_.verify_post)])


# Fetch all comments associated with one post
@router.get('/all')
async def get_comments(post_id: str, page: dict = Depends(_.pagination)):
    # find_many({"post_id": post_id})
    comments = await Comment.aggregate(
        [{'$match': {'post_id': ObjectId(post_id)}}, {'$skip': page['skip'] * page['limit']},
         {'$limit': page['limit']}],
        projection_model=Comment).to_list()
    if comments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No comments on this post")
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"comments": jsonable_encoder(comments)})


# Publish one comment associated to one post
@router.post('/')
async def post_comment(post_id: str, comment_msg: CommentModel, user: User = Depends(_.authorized_user)):
    comment = Comment(**comment_msg.__dict__, post_id=post_id, comment_by=user.id,
                      created_by=datetime.datetime.now())
    comment = await comment.create()
    if comment is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Couldn't post comment")
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"users": jsonable_encoder(comment)})
