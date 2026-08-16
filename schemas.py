from pydantic import BaseModel, Field
from typing import Literal

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
    amount: float = Field(gt =0)
    category: Literal["income", "expense"]
    name: str = Field(min_length = 1, max_length = 100)
    description: str | None = Field(default = None, max_length = 255)


class TransactionUpdate(BaseModel):
    amount: float | None = Field(default = None, gt = 0)
    category: str | None = None
    name: str | None = Field(default=None, min_length = 1)
    description: str | None = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    category: str
    name: str
    description: str | None

    class Config:
        from_attributes = True