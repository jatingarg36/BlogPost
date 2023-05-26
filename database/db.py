from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import CONFIG
from models.comment import Comment
from models.post import Post
from models.user import User

''' 
Initiating Database Instance
'''


async def initiate_database():
    # Connecting to DB_URL
    print(CONFIG.DATABASE_URL)
    client = AsyncIOMotorClient(CONFIG.DATABASE_URL)

    try:
        '''Ping for  confirm a successful connection'''
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return await init_beanie(database=client[CONFIG.DATABASE], document_models=[User, Post, Comment])
    except Exception as e:
        print(e)
