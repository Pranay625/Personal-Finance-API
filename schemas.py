from pydantic import BaseModel, Field
from typing import Literal
from datetime import date
from decimal import Decimal


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    type: Literal["income", "expense"]
    category_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    transaction_date: date


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0)
    type: Literal["income", "expense"] | None = None
    category_id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    transaction_date: date | None = None


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: Decimal
    type: str
    name: str
    description: str | None
    transaction_date: date

    class Config:
        from_attributes = True