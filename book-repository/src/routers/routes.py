from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
  prefix="/api/v1/pg",
  tags=["bookstore"]
)

@router.get("/health")
async def health_check():
    ''' For service healthcheck '''
    item = JSONResponse(content={"status": "healthy"}, 
                        status_code=status.HTTP_200_OK, 
                        media_type="application/json")
    return item

@router.get("/query")
async def sql_db_guery():
    print('Sends query to database for execution')
    