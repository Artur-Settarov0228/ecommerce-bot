from sqlalchemy import select
from database.session import SessionLocal
from database.models.product import Product

class ProductService:

    @staticmethod
    async def create(name: str, price: int, stock: int):
        async with SessionLocal() as session:
            product = Product(
                name=name,
                price=price,
                stock=stock,
                is_active=True,
            )
            session.add(product)
            await session.commit()

    @staticmethod
    async def get_all():
        async with SessionLocal() as session:
            result = await session.execute(
                select(Product).where(Product.is_active == True)
            )
            return result.scalars().all()
