from sqlalchemy import select
from database.session import SessionLocal
from database.models.card_item import CartItem
from database.models.order import Order
from database.models.order_item import OrderItem

class OrderService:

    @staticmethod
    async def checkout(user_id: int):
        async with SessionLocal() as session:
            # 1) CartItemlarni olish
            result = await session.execute(
                select(CartItem).where(CartItem.user_id == user_id)
            )
            cart_items = result.scalars().all()

            if not cart_items:
                return None

            # 2) Total hisoblash
            total = 0
            for item in cart_items:
                total += item.product.price * item.quantity

            # 3) Order yaratish
            order = Order(
                user_id=user_id,
                total_price=total,
                status="new"
            )
            session.add(order)
            await session.flush()  # order.id olish uchun

            # 4) OrderItemlar yaratish
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity
                )
                session.add(order_item)

            # 5) Cart tozalash
            for item in cart_items:
                await session.delete(item)

            await session.commit()
            return order
