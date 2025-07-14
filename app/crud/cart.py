from sqlalchemy.orm import Session


from app.db.models.cart import  Cart
from app.db.models.cart_item import CartItem
from app.schemas.cart import CartItemCreate

def get_cart(db: Session, cart_id: int) -> Cart | None:
    return db.query(Cart).filter(Cart.id == cart_id).first()

def get_cart_by_user(db: Session, user_id: int) -> Cart | None:
    return db.query(Cart).filter(Cart.user_id == user_id).first()

def create_cart(db: Session, user_id: int) -> Cart:
    db_cart = Cart(user_id=user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def add_item_to_cart(
    db: Session,
    cart: Cart,
    item_in: CartItemCreate
) -> CartItem:
    db_item = CartItem(
        cart_id=cart.id,
        product_id=item_in.product_id,
        quantity=item_in.quantity
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_item_from_cart(
    db: Session,
    cart_item: CartItem
) -> None:
    db.delete(cart_item)
    db.commit()
