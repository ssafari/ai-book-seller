from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    isbn: str
    price: float
    count: int
    customer: str