from fastapi import Depends
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from src.repository.abstract_repository import AbstractUserRepository as UserRepositoryInterface
from src.service.user_services import UserService
from repository.users_repository import UserRepositoryImpl as UserRepository


# Define your MongoDB connection URL
MONGO_DB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "book-seller"
USER_COLLECTION = "user-info"


async def get_mdb_client():
    """ get the db client """
    client = AsyncMongoClient(MONGO_DB_URL)
    try:
        yield client
    finally:
        await client.close()

async def get_mdb_collection(client: AsyncMongoClient = Depends(get_mdb_client)) -> AsyncCollection:
    """ get connection """
    db = client[DATABASE_NAME]
    return db[USER_COLLECTION]

async def get_user_repository(mdb: AsyncCollection = Depends(get_mdb_collection)) -> UserRepositoryInterface:
    return UserRepository(mdb)

async def get_user_service(user_repository: UserRepositoryInterface = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)
