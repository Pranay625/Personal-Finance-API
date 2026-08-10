from sqlalchemy import Column, Integer, String, Float
from db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String(20))
    category = Column(String(100))
    description = Column(String(255))