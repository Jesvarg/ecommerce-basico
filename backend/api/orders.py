import products as products
from typing import Optional
from models import Order, OrderItem
from database import db


def create_order(user_id: int, total: float, status: str,
                 shipping_address: str, payment_method: str,
                 items_data: list[dict]) -> Order:
    """
    Crear una orden con ítems
    :param items_data: lista de dicts con 'product_id', 'quantity', 'price_at_purchase'
    """
    order = Order(
        user_id=user_id,
        total=total,
        status=status,
        shipping_address=shipping_address,
        payment_method=payment_method
    )

    for item in items_data:
        product = products.get_product_by_id(item["product_id"])
        if not product or product.stock < item["quantity"]:
            raise ValueError(f"Stock insuficiente para producto {item['product_id']}")

        # Restar stock
        product.stock -= item["quantity"]
        db.session.add(product)

        # Crear ítem de orden
        order_item = OrderItem(
            product_id=item["product_id"],
            quantity=item["quantity"],
            price_at_purchase=item["price_at_purchase"],
            subtotal=item["quantity"] * item["price_at_purchase"]
        )
        order.order_items.append(order_item)

    db.session.add(order)
    db.session.commit()

    return order


def get_orders_by_user(user_id: int) -> list[Order]:
    return Order.query.filter_by(user_id=user_id).all()


def get_order_by_id(order_id: int) -> Optional[Order]:
    return Order.query.get(order_id)


def update_order_status(order_id: int, new_status: str) -> Order:
    order = get_order_by_id(order_id)
    if not order:
        raise ValueError("Orden no encontrada")
    
    order.status = new_status
    db.session.commit()
    return order


def cancel_order(order_id: int) -> None:
    order = get_order_by_id(order_id)
    if not order:
        raise ValueError("Orden no encontrada")
    
    # Devolver stock
    for item in order.order_items:
        product = products.get_product_by_id(item.product_id)
        if product:
            product.stock += item.quantity
            db.session.add(product)

    order.status = "cancelled"
    db.session.commit()