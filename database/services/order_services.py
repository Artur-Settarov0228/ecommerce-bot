from sqlalchemy import select
from database.session import SessionLocal
from database.models.card_item import CartItem
from database.models.order import Order
from database.models.order_item import OrderItem
from config import settings

class OrderService:

    @staticmethod
    async def checkout(user_id: int, name: str, phone: str):
        async with SessionLocal() as session:
            result = await session.execute(
                select(CartItem).where(CartItem.user_id == user_id)
            )
            cart_items = result.scalars().all()

            if not cart_items:
                return None

            total = sum(
                item.product.price * item.quantity for item in cart_items
            )

            order = Order(
                user_id=user_id,
                total_price=total,
                status="new",
            )
            session.add(order)
            await session.flush()

            for item in cart_items:
                session.add(
                    OrderItem(
                        order_id=order.id,
                        product_name=item.product.name,
                        product_price=item.product.price,
                        quantity=item.quantity,
                    )
                )
                await session.delete(item)

            await session.commit()
            return order
