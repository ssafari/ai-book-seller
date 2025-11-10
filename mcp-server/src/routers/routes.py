from fastapi import APIRouter, HTTPException, Query
import httpx



router = APIRouter(
    prefix="/api/v1/mcp",
    tags=["mcp"]
)

