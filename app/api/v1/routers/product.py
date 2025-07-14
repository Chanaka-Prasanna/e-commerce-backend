# app/api/v1/routers/products.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.crud.product import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product,
)
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=ProductRead)
def create_product_endpoint(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
):
    return create_product(db, product_in)

@router.get("/", response_model=List[ProductRead])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductRead)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductRead)
def update_product_endpoint(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return update_product(db, product, product_in)

@router.delete("/{product_id}", response_model=ProductRead)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return delete_product(db, product)
