import asyncio

from database.connection import engine
from database.models.base import BaseModel
from database.models import (
    user,
    category,
    product,
    card_item,
    order,
    order_item,
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
