from abc import ABC, abstractmethod
from src.models.book import Book


class AbstractBookRepository(ABC):

    @abstractmethod
    async def find_book(self, isbn: str) -> Book:
        pass

    @abstractmethod
    async def add_book(self, book: Book):
        pass

    @abstractmethod
    async def update_book(self, book: Book):
        pass
    
    @abstractmethod
    async def delete_book(self, isbn: str):
        pass