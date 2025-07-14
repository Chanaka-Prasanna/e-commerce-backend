# app/api/v1/routers/carts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.cart import CartCreate, CartRead, CartItemCreate, CartItemRead
from app.crud.cart import (
    get_cart,
    get_cart_by_user,
    create_cart,
    add_item_to_cart,
    remove_item_from_cart,
)
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=CartRead)
def create_cart_endpoint(
    cart_in: CartCreate,
    db: Session = Depends(get_db),
):
    return create_cart(db, cart_in.user_id)

@router.get("/user/{user_id}", response_model=CartRead)
def read_cart_by_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    cart = get_cart_by_user(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/{cart_id}/items", response_model=CartItemRead)
def add_item(
    cart_id: int,
    item_in: CartItemCreate,
    db: Session = Depends(get_db),
):
    cart = get_cart(db, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return add_item_to_cart(db, cart, item_in)

@router.delete("/items/{item_id}", response_model=dict)
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    from app.db.models.cart_item import CartItem
    item = db.query(CartItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    remove_item_from_cart(db, item)
    return {"detail": "Item removed"}
