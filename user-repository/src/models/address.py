from pydantic import BaseModel

class Address(BaseModel):
    number: int
    street: str
    city: str
    state: str
    code: int
    unit: int
    suite: int
    appt: int