import asyncio
from langchain_postgres import PGEngine
from langchain_community.utilities import SQLDatabase
from sqlalchemy import text, inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from src.repository.book import Base, Book

class PgClient:
    ''' creates client connection to the database'''

    CONNECTION_STRING = "postgresql+asyncpg://postgres:postgres@localhost:5432/"
    #TABLE_NAME = "bdf_bookstore"
    VECTOR_SIZE = 768
    #db_name = "projects"
    pg_engine: PGEngine
    engine: AsyncEngine

    def __init__(self, table, db):
        # Create an SQLAlchemy Async Engine
        self.table_name = table
        database = self.CONNECTION_STRING+db
        self.engine = create_async_engine(
            #self.CONNECTION_STRING,
            database,
        )
        print("create database engine")
        self.pg_engine = PGEngine.from_engine(engine=self.engine)
        self.async_session = async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                expire_on_commit=False
        )
        
    async def get_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(lambda conn: SQLDatabase(engine=conn))

    async def create_books_table(self):
        ''' create table with traditional methods'''
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    
    async def execute_sql_query(self) -> str:
        """Executes a SQL query and returns the results."""
        async with self.async_session() as session:
            try:
                result = await session.execute(text("SELECT title FROM books WHERE category = 'fiction' LIMIT 3;"))
                # Process result as needed, e.g., fetch all rows
                print(f"===> output {str(result.scalars().all())}")
                return str(result.fetchall())
            except Exception as e:
                return f"Error executing query: {e}"

    async def get_table_names(self):
        async with self.engine.connect() as conn:
            table_names = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
            return table_names
            
    def get_table_schema(self):
        ''' Returns name of columns'''
        print("pgclient get_table_schema")
        return [column.name for column in Book.__table__.columns]
        # async with self.engine.connect() as conn:
        #     metadata = Base.metadata
        #     table = await conn.run_sync(
        #         lambda sync_conn: Table(self.TABLE_NAME, metadata, autoload_with=sync_conn)
        #     )
        #     return table.columns
        
async def async_main() -> None:
    ''' main function for running async methods '''
    print("\n Start PGClient ... \n")
    client = PgClient("books", "bookstore.db")
    await client.create_books_table()
    #await client.execute_sql_query()

    # table_names = await client.get_table_schema()
    # print(table_names)
    column_names = [column.name for column in Book.__table__.columns]
    print(column_names)

if __name__ == "__main__":
    asyncio.run(async_main())
