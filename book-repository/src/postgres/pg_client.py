import asyncio
from langchain_postgres import PGEngine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from src.repository.book import Base

class PgClient:
    ''' creates client connection to the database'''

    CONNECTION_STRING = "postgresql+asyncpg://postgres:postgres@localhost:5432/projects"
    TABLE_NAME = "books"
    VECTOR_SIZE = 768
    db_name = "projects"
    pg_engine: PGEngine
    engine: AsyncEngine

    def __init__(self):
        # Create an SQLAlchemy Async Engine
        self.engine = create_async_engine(
            self.CONNECTION_STRING,
        )
        print("create database engine")
        self.pg_engine = PGEngine.from_engine(engine=self.engine)
        #db = SQLDatabase.from_uri(self.pg_uri)

    async def create_books_table(self):
        ''' create table with traditional methods'''
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

async def async_main() -> None:
    ''' main function for running async methods '''
    print("\n Start PGClient ... \n")
    client = PgClient()
    await client.create_books_table()
    

if __name__ == "__main__":
    asyncio.run(async_main())
