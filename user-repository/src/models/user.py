from pydantic import BaseModel
from address import Address

class User(BaseModel):
    first_name: str
    last_name: str
    email_addr: str
    card_number: int
    last_purchase: str
    address: Address
