import logging
from src.repository.abstract_repository import AbstractBookRepository
from src.models.book import Book
from src.exceptions import BaseAppException, ResourceNotFoundException

class BookService:

    def __init__(self, book_repository: AbstractBookRepository):
        self.repository = book_repository
    

    async def get_book(self, isbn: str) -> Book:
        try:
            result = await self.repository.find_book(isbn)
            if not result:
                raise ResourceNotFoundException(f"Book with isbn {isbn} not found")
            return
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logging.exception("Error finding book: %s", str(e))
            raise BaseAppException(f"Internal database error: {str(e)}") from e
    
    async def add_book(self, book: Book) -> Book:
        try:
            id = await self.repository.add_book(book)
            return id
        except Exception as e:
            logging.error("Error inserting document from source: %s", e)
            raise BaseAppException(f"Internal database error: {str(e)}") from e

    
    async def update_book(self, pbook: Book) -> Book:
        book = await self.repository.find_book(pbook.isbn)
        if book:
            book.price = pbook.price
            await self.repository.update_book(book)
        
        return book

    
    async def delete_book(self, isbn: str) -> bool:
        await self.repository.delete_book(isbn=isbn)
        return True