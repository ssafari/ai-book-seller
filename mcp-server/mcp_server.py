from fastmcp import FastMCP
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from starlette.requests import Request
from starlette.responses import PlainTextResponse

# Initialize your FastMCP server
mcp = FastMCP(name="book-store-tools")

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/bookstore.db"

async def get_pgsql_conn():
    ''' Get db async connection '''
    async_engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=async_engine,
                    class_=AsyncSession
    )
    return async_session


@mcp.tool(name='execute_sql_query_async', 
          description='sends sql query to database')
async def execute_sql_query_async(query: str) -> str:
    """Executes a SQL query and returns the results."""
    print(f"SQL query: {query}")
    async_session = await get_pgsql_conn()
    async with async_session() as session:
        try:
            result = await session.execute(text(query))
            # Process result as needed, e.g., fetch all rows
            #return str(result.scalars().all())
            rows = result.fetchall()
            return str([row[0] for row in rows])
        except Exception as e:
            return f"Error executing query: {e}"


@mcp.tool(name='get_tables_name',
          description='get the name of tables in database')
async def get_tables_name() -> list[str]:
    ''' Get table names'''
    async_session = await get_pgsql_conn()
    async with async_session() as session:
        result = await session.execute(text("""
                                                SELECT table_name 
                                                FROM information_schema.tables 
                                                WHERE table_schema = 'public';
                                            """))
        rows = result.fetchall()
        return [row[0] for row in rows]


@mcp.tool(name='get_table_schema', 
          description='get table schema')
async def get_table_schema(t_name: str) -> list:
    '''get table schema'''
    async_session = await get_pgsql_conn()
    async with async_session() as session:
        result = await session.execute(text(f"""
                                                SELECT column_name 
                                                FROM information_schema.columns 
                                                WHERE table_schema = 'public' 
                                                AND table_name = '{t_name}';
                                            """
                                            )
                                        )
        #print(str(result.scalars().all()))
        rows = result.fetchall()
        return [row[0] for row in rows]


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    ''' Checks mcp server runing'''
    return PlainTextResponse("Tools Server is OK")


# Run the server
if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8003)

