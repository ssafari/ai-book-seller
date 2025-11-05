import logging
from src.repository.abstract_repository import AbstractUserRepository
from src.models.user import User
from src.exceptions import BaseAppException, ResourceNotFoundException

class UserService:

    def __init__(self, user_repository: AbstractUserRepository):
        self.repository = user_repository
    

    async def get_user(self, isbn: str) -> User:
        try:
            result = await self.repository.find_user(isbn)
            if not result:
                raise ResourceNotFoundException(f"User with isbn {isbn} not found")
            return
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logging.exception("Error finding user: %s", str(e))
            raise BaseAppException(f"Internal database error: {str(e)}") from e
    
    async def add_user(self, user: User) -> User:
        try:
            id = await self.repository.add_user(user)
            return id
        except Exception as e:
            logging.error("Error inserting document from source: %s", e)
            raise BaseAppException(f"Internal database error: {str(e)}") from e

    
    async def update_user(self, puser: User) -> User:
        user = await self.repository.find_user(puser.isbn)
        if user:
            user.price = puser.price
            await self.repository.update_user(user)
        
        return user

    
    async def delete_user(self, isbn: str) -> bool:
        await self.repository.delete_user(isbn=isbn)
        return True