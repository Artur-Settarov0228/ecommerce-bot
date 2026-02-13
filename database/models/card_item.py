from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class CartItem(BaseModel):
    __tablename__ = "cart_items"

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )
    quantity = Column(Integer, nullable=False)

    user = relationship("User")
    product = relationship("Product")
