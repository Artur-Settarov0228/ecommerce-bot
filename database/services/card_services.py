from sqlalchemy import select, delete
from database.session import SessionLocal
from database.models.card_item import CartItem
from database.models.product import Product

class CartService:

    @staticmethod
    async def add(user_id: int, product_id: int, qty: int = 1):
        async with SessionLocal() as session:
            result = await session.execute(
                select(CartItem).where(
                    CartItem.user_id == user_id,
                    CartItem.product_id == product_id
                )
            )
            cart_item = result.scalar_one_or_none()

            if cart_item:
                cart_item.quantity += qty
            else:
                cart_item = CartItem(
                    user_id=user_id,
                    product_id=product_id,
                    quantity=qty
                )
                session.add(cart_item)

            await session.commit()

    @staticmethod
    async def get_cart(user_id: int):
        async with SessionLocal() as session:
            result = await session.execute(
                select(CartItem).where(CartItem.user_id == user_id)
            )
            return result.scalars().all()

    @staticmethod
    async def clear(user_id: int):
        async with SessionLocal() as session:
            await session.execute(
                delete(CartItem).where(CartItem.user_id == user_id)
            )
            await session.commit()
