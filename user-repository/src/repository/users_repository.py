from pymongo.asynchronous.collection import AsyncCollection
from src.repository.abstract_repository import AbstractUserRepository
from src.models.user import User

class UserRepositoryImpl(AbstractUserRepository):
    """
        This is the MongoDB repository implementation
    """
    
    def __init__(self, db: AsyncCollection):
        self.db = db

    async def find_user(self, isbn: str) -> User:
            return await self.db.find_one(isbn)
            
  
    async def add_user(self, user: User):
        document = {
            "_id": user.email_addr,
            "fname": user.first_name,
            "lname": user.last_name,
            "card": user.card_number,
            "addr": user.address
        }
        result = await self.db.insert_one(document)
        return result.inserted_id
        

    async def update_user(self, user: User) -> User:
        return await self.db.insert_one(user)
    
    
    async def delete_user(self, email: str):
        await self.db.delete_one(email)