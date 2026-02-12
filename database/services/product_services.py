from sqlalchemy import select
from database.session import SessionLocal
from database.models.product import Product

class ProductService:

    @staticmethod
    async def get_all():
        async with SessionLocal() as session:
            result = await session.execute(
                select(Product).where(Product.is_active == True)
            )
            return result.scalars().all()
