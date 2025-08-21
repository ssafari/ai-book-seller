from pydantic import BaseModel

class Book(BaseModel):
    isbn: str
    title: str
    price: str
    type_: str

    # def __init__(self, isbn, title, price, type_):
    #     """ """
    #     super().__init__()
    #     self.isbn = isbn
    #     self.title = title
    #     self.price = price
    #     self.type_ = type_

    # def get_isbn(self):
    #     return self.isbn
    
    # def get_title(self):
    #     return self.title
    
    # def get_price(self):
    #     return self.price
    
    # def set_price(self, newPrice):
    #     self.price = newPrice

    # def set_type(self, newType):
    #     self.type_ = newType
