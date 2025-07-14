from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .product import ProductRead

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemRead(CartItemBase):
    id: int
    # include nested product info if you like:
    product: Optional[ProductRead]

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class CartRead(CartBase):
    id: int
    items: List[CartItemRead] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
