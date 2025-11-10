from asyncio.log import logger
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from fastapi.middleware.cors import CORSMiddleware
from src.routers import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code (runs before application startup)
    logger.info("Running startup tasks...")
    logger.info("Startup tasks completed")
    yield
    # Shutdown code (runs after application shutdown)
    logger.info("Running shutdown tasks...")
    logger.info("Shutdown tasks completed")
    # This is where you put code that was previously in @app.on_event("shutdown")


app = FastAPI(title="Updates API", lifespan=lifespan)
app.include_router(routes.router)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["Authorization", "Content-Type"]
)

mcp = FastApiMCP(
   app,
   name="Weather Updates API",
   description="API for retrieving today's weather from weather.gov",
)
mcp.mount()


# def main():
#     print("Hello from mcp-server!")


# if __name__ == "__main__":
#     main()
