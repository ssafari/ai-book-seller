import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import routes


# Configure basic logging for application
logging.getLogger("asyncio").setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Must us init codes here before application startup
    logging.info("*** Starting book-repository application...")
    yield
    # Shutdown code (runs after application shutdown)
    logging.info("*** Shutdown book-repository completed")
    # This is where you put code that was previously in @app.on_event("shutdown")
    # define a lifespan method for fastapi


app = FastAPI(lifespan=lifespan)
#app.include_router(routes.router)

origins = [
    "http://localhost:8005",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)

