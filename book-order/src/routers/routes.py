# routers/items.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/order",
    tags=["order"]
)

@router.get("/")
async def read_orders():
    return [{"name": "Item Foo"}, {"name": "Item Bar"}]

@router.get("/{order_id}")
async def read_item(order_id: int):
    return {
        "order_id": order_id,
        "isbn": "948434923883",
        "price": 24.5,
        "count": 1
        }