from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from datetime import datetime
import anyio

from app.utils.publisher import publish_event

router = APIRouter()

class Item(BaseModel):
    sku: str
    qty: int
    unit_price: float

class OrderEvent(BaseModel):
    vendor_id: str
    order_id: str
    items: List[Item]
    timestamp: datetime

@router.post("/")
async def ingest_event(event: OrderEvent):
    try:
        data = event.dict()
        data["id"] = str(uuid4())
        data["timestamp"] = data["timestamp"].isoformat()
        await anyio.to_thread.run_sync(publish_event, data)
        return {"message":"Event published","event_id":data["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))