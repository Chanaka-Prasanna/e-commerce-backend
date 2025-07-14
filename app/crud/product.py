from sqlalchemy.orm import Session

from app.db.models.product import  Product
from app.schemas.product import ProductUpdate, ProductCreate

def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product_in: ProductCreate) -> Product:
    db_product = Product(**product_in.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(
    db: Session,
    db_product: Product,
    product_in: ProductUpdate
) -> Product:
    for field, value in product_in.dict(exclude_unset=True).items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: Product) -> Product:
    db.delete(db_product)
    db.commit()
    return db_product
