from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    category = relationship("Category")
