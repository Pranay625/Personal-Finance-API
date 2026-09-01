from sqlalchemy import Column, Integer, String, ForeignKey, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    transactions = relationship("Transaction", back_populates="owner")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    amount = Column(DECIMAL(10, 2), nullable=False)

    type = Column(String(10), nullable=False)

    name = Column(String(100), nullable=False)

    description = Column(String(255))

    transaction_date = Column(Date, nullable=False)

    created_at = Column(TIMESTAMP)

    updated_at = Column(TIMESTAMP)

    owner = relationship("User", back_populates="transactions")

    category = relationship("Category", back_populates="transactions")