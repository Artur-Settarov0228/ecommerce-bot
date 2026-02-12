from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"

    parent_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True
    )
    name = Column(String(255), nullable=False)

    parent = relationship("Category", remote_side="Category.id")
