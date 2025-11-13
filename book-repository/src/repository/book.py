from pgvector.sqlalchemy import Vector
#from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, String, DOUBLE_PRECISION, BigInteger, TEXT
from sqlalchemy.ext.declarative import declarative_base


# Create a declarative base class
Base = declarative_base()

# Define the Book model
class Book(Base):
    ''' Book Store table '''
    __tablename__ = 'bdf_bookstore'

    isbn = Column(BigInteger, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    genre = Column(String(100))
    description = Column(TEXT)
    rating = Column(DOUBLE_PRECISION)
    meta_data = Column(TEXT)
    embedding = Column(Vector(768))

    def __init__(self):
        pass

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', genre='{self.genre}')>"

