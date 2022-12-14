from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, Numeric
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
