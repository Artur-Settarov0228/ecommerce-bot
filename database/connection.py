from sqlalchemy.ext.asyncio import create_async_engine
from config import DB_HOST, DB_NAME, DB_PASS,DB_PORT, DB_USER

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:"
    f"{DB_PASS}@{DB_HOST}:"
    f"{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)
