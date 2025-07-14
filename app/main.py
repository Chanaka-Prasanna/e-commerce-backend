from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# 1️⃣ Use Base from your db package
from app.db.base import Base
from app.db.session import engine, get_db

# 2️⃣ Import all model classes so they register with Base.metadata
from app.db.models.user import User
from app.db.models.product import Product
from app.db.models.cart import Cart
from app.db.models.cart_item import CartItem
from app.db.models.order import Order
from app.db.models.order_item import OrderItem

# 3️⃣ Auto-create all tables on startup
Base.metadata.create_all(bind=engine)

# 4️⃣ Instantiate FastAPI with OpenAPI tags
app = FastAPI(
    title="E-Commerce Backend",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
        {"name": "users", "description": "Operations with users"},
        {"name": "products", "description": "Operations with products"},
        {"name": "carts", "description": "Operations with carts"},
        {"name": "orders", "description": "Operations with orders"},
    ],
)

# 5️⃣ Include your versioned routers
from app.api.v1.routers.user import router as users_router
from app.api.v1.routers.product import router as products_router
from app.api.v1.routers.cart import router as carts_router
from app.api.v1.routers.order import router as orders_router

app.include_router(
    users_router,
    prefix="/api/v1/users",
    tags=["users"],
)
app.include_router(
    products_router,
    prefix="/api/v1/products",
    tags=["products"],
)
app.include_router(
    carts_router,
    prefix="/api/v1/carts",
    tags=["carts"],
)
app.include_router(
    orders_router,
    prefix="/api/v1/orders",
    tags=["orders"],
)

# 6️⃣ Health endpoints
@app.get("/", tags=["health"])
def root():
    return {"message": "Welcome to E-Commerce API"}

@app.get("/health/db", tags=["health"])
def health_check(db: Session = Depends(get_db)):
    """
    Verifies database connectivity by running SELECT 1.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"db_status": "healthy"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="DB connection failed")
