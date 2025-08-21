from fastapi import Depends
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from src.repository.abstract_repository import AbstractBookRepository as BookRepositoryInterface
from src.service.book_service import BookService
from src.repository.mongodb_book_repository import BookRepositoryMongodbImpl as MongodbBookRepository


# Define your MongoDB connection URL
MONGO_DB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "ai-project"
BOOK_COLLECTION = "book-seller"


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
    return db[BOOK_COLLECTION]

async def get_book_repository(mdb: AsyncCollection = Depends(get_mdb_collection)) -> BookRepositoryInterface:
    return MongodbBookRepository(mdb)

async def get_book_service(book_repository: BookRepositoryInterface = Depends(get_book_repository)) -> BookService:
    return BookService(book_repository)
