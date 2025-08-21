from pymongo.asynchronous.collection import AsyncCollection
from src.repository.abstract_repository import AbstractBookRepository
from src.models.book import Book

class BookRepositoryMongodbImpl(AbstractBookRepository):
    """
        This is the MongoDB repository implementation
    """
    
    def __init__(self, db: AsyncCollection):
        self.db = db

    async def find_book(self, isbn: str) -> Book:
            return await self.db.find_one(isbn)
            
  
    async def add_book(self, book: Book):
        document = {
            "_id": book.isbn,
            "title": book.title,
            "price": book.price,
            "type": book.type_
        }
        result = await self.db.insert_one(document)
        return result.inserted_id
        

    async def update_book(self, book: Book) -> Book:
        return await self.db.insert_one(book)
    
    
    async def delete_book(self, isbn: str):
        await self.db.delete_one(isbn)