from sqlalchemy.orm import Session

from app.db.models.order import  Order
from app.db.models.order_item import OrderItem
from app.schemas.order import OrderCreate

def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders_by_user(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()

def create_order(db: Session, order_in: OrderCreate) -> Order:
    # 1) create the order record
    db_order = Order(
        user_id=order_in.user_id,
        status=order_in.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # 2) create each item, calculate total
    total = 0.0
    for item in order_in.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.price_at_purchase
        )
        db.add(db_item)
        total += item.quantity * item.price_at_purchase

    # 3) update total amount
    db_order.total_amount = total
    db.commit()
    db.refresh(db_order)

    return db_order
