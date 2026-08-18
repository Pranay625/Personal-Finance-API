from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(50), unique = True, nullable = False)
    password = Column(String(255), nullable = False)
    transactions = relationship("Transaction", back_populates="owner")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    category = Column(String(20))
    name = Column(String(100))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    owner = relationship("User", back_populates="transactions")