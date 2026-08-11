from sqlalchemy import Column, Integer, String, Float
from db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    category = Column(String(20))
    name = Column(String(100))
    description = Column(String(255))