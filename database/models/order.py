from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Order(BaseModel):
    __tablename__ = "orders"

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    total_price = Column(Integer, nullable=False)
    status = Column(String(20), default="new")

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
