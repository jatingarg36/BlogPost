from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

'''
Using a HTTP Bearer to get the request
and pass it on to AuthJWT for validating
headers with jwt token
'''
class JWT_Bearer(HTTPBearer):

    def __init__(self):
        super(JWT_Bearer, self).__init__()

    async def __call__(self, req: Request):
        print(req.headers)
        auth = AuthJWT(req=req)
        print(auth.get_jwt_subject())
        return auth
