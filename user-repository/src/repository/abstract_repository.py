from abc import ABC, abstractmethod
from src.models.user import User


class AbstractUserRepository(ABC):

    @abstractmethod
    async def find_user(self, isbn: str) -> User:
        pass

    @abstractmethod
    async def add_user(self, user: User):
        pass

    @abstractmethod
    async def update_user(self, user: User):
        pass
    
    @abstractmethod
    async def delete_user(self, isbn: str):
        pass