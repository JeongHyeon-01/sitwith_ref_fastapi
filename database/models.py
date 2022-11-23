from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, Numeric
from sqlalchemy.orm import relationship

from .databases import Base

class BaseMixin:
    id = Column(Integer, primary_key = True, index =True)
    created_at = Column(DateTime, default=func.utc_timestamp())
    updated_at = Column(DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

class User(Base, BaseMixin):
    __tablename__ = "users"
    
    username = Column(String(120), nullable = False)
    password = Column(String(255), nullable = False)
    email = Column(String(255), unique=True, nullable = False)
    is_activate = Column(Boolean, default = True)
    
#     carts = relationship("Cart", back_populates = "users")

# class Category(Base, BaseMixin):
#     __tablename__ = "category"
    
#     name = Column(String, nullable = False)
    
#     products =relationship("Product", back_populates="categories") 
    
# class Product(Base, BaseMixin):
#     __tablename__ = "products"
    
#     name = Column(String, nullable = False)
#     price = Column(Numeric(precision=3,scale=2),nullable = False)

#     category_id = Column(Integer, ForeignKey("categoery.id"))
#     categories = relationship("Category", back_populates = "products")
#     productsbycolors = relationship("ProductsbyColor", back_populates="products")

# class Color(Base, BaseMixin):
#     __tablename__ = "colors"
    
#     name = Column(String, nullable = False)
    
#     productsbycolors = relationship("ProductsbyColor", back_populates="colors")
    
# class ProductsbyColor(Base, BaseMixin):
#     __tablename__ = "productsbycolors"
    
#     inventory = Column(Integer, nullable = False)
    
#     colors = relationship("Color", back_populates="productsbycolors")
#     products = relationship("Product", back_populates = "productsbycolors")
    
#     carts = relationship("Cart", back_populates = "productsbycolors")
    
# class Cart(Base, BaseMixin):
#     __tablename__ = "carts"
    
#     count = Column(Integer, nullable = False)
    
#     productsbycolors = relationship("ProductsbyColor", back_populates = "carts")
#     users = relationship("User",back_populates = "carts")