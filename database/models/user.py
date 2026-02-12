from sqlalchemy import Column, BigInteger, String
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    language = Column(String(5), default="uz")
