from sqlalchemy import Column, String, Text, DOUBLE_PRECISION, BigInteger
from sqlalchemy.ext.declarative import declarative_base


# Create a declarative base class
Base = declarative_base()

# Define the Book model
class Book(Base):
    ''' Book Store table '''
    __tablename__ = 'books'

    isbn = Column(BigInteger, primary_key=True)
    title = Column(String(250), nullable=False)
    authors = Column(String(250), nullable=False)
    categories = Column(String(100))
    description = Column(Text)
    rating = Column(DOUBLE_PRECISION)
    content = Column(Text)

    def __init__(self):
        pass

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.authors}', genre='{self.categories}')>"

