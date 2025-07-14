# app/api/v1/routers/orders.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.order import OrderCreate, OrderRead
from app.crud.order import get_order, get_orders_by_user, create_order
from app.db.session import get_db


router = APIRouter()

@router.post("/", response_model=OrderRead)
def create_order_endpoint(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
):
    return create_order(db, order_in)

@router.get("/{order_id}", response_model=OrderRead)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/user/{user_id}", response_model=List[OrderRead])
def read_orders_by_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_orders_by_user(db, user_id)
