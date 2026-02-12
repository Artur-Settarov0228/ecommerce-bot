from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    product_name = Column(String(255), nullable=False)
    product_price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
