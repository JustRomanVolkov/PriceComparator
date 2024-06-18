from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from .database import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="store")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price_new = Column(Float)
    price_old = Column(Float, nullable=True)
    article = Column(String, index=True, nullable=True)
    rating = Column(Float, nullable=True)
    availability = Column(String, nullable=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    store = relationship("Store", back_populates="products")
    category = relationship("Category", back_populates="products")


class StoreCreate(BaseModel):
    name: str


class CategoryCreate(BaseModel):
    name: str


class ProductCreate(BaseModel):
    name: str
    description: str = None
    price_new: float
    price_old: float = None
    article: str = None
    rating: float = None
    availability: str = None
    store_id: int
    category_id: int

    class Config:
        from_attributes = True
