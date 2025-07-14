from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .product import ProductRead

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    product: Optional[ProductRead]

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int
    status: str  # e.g. "pending", "completed"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderRead(OrderBase):
    id: int
    items: List[OrderItemRead] = []
    total_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
