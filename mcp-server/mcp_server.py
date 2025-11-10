from fastmcp import FastMCP
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from starlette.requests import Request
from starlette.responses import PlainTextResponse

# Initialize your FastMCP server
mcp = FastMCP(name="MCP Tools Server")

async def get_pgsql_conn():
    async_engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/projects"
    )
    async_session = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=async_engine,
                    class_=AsyncSession
    )
    return async_session


@mcp.tool
async def execute_sql_query_async(query: str) -> str:
    """Executes a SQL query and returns the results."""
    #print(f"SQL query: {query}")
    async_session = await get_pgsql_conn()
    async with async_session() as session:
        try:
            result = await session.execute(text(query))
            # Process result as needed, e.g., fetch all rows
            return str(result.fetchall()) 
        except Exception as e:
            return f"Error executing query: {e}"
        

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("Tools Server is OK")


# Run the server
if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)