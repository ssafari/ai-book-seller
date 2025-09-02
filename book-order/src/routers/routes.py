from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.produce.producer import KafkaProducer
from src.models.order import Order

router = APIRouter(
    prefix="/api/v1/order",
    tags=["order"]
)

@router.get("/health")
async def health_check():
    ''' For service healthcheck '''
    item = JSONResponse(content={"status": "healthy"}, 
                        status_code=status.HTTP_200_OK, 
                        media_type="application/json")
    return item

@router.post("/")
async def read_item(book_order: Order):
    ''' receviing order and sending it to shipping handling'''
    data = jsonable_encoder(book_order)
    item = JSONResponse(content=data)
    kafka = KafkaProducer()
    kafka.send_book_order(item.body)
    return JSONResponse(content=data, 
                        status_code=status.HTTP_201_CREATED, 
                        media_type="application/json")
