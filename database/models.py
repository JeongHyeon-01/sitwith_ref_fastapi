from sqlalchemy import Boolean, Column, ForeignKey, \
    Integer, String, DateTime, func, Float, Numeric
from sqlalchemy.orm import relationship
from .databases import Base

class User(Base):
    __tablename__ = "users"
        
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(120), unique=True,nullable = False)
    password = Column(String(255), nullable = False)
    email = Column(String(255), unique=True, nullable = False)
    is_activate = Column(Boolean, default = True)
    created_at = Column(DateTime, default=func.utc_timestamp())
    updated_at = Column(DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), unique=True, index=True, nullable = False)

    products = relationship("Product", back_populates = "categories")
    
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable = False)
    price = Column(Float(precision=3,asdecimal=True),nullable = False)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"))
    categories  = relationship("Category", back_populates = "products")
    
    productcolors = relationship("ProductColor", back_populates = "products")
    
class Color(Base):
    __tablename__ = "colors"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable = False)
    
    colorsproduct = relationship("ProductColor", back_populates = "colors")
    
class ProductColor(Base):
    __tablename__ = "productcolors"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inventory = Column(Integer, default=0)
    color_id = Column(Integer, ForeignKey("colors.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    colors = relationship("Color", back_populates="colorsproduct")
    products = relationship("Product", back_populates="productcolors")
