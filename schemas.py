from pydantic import BaseModel, Field
from typing import Literal

class TransactionCreate(BaseModel):
    amount: float = Field(gt =0)
    category: Literal["income", "expense"]
    name: str = Field(min_length = 1, max_length = 100)
    description: str | None = Field(default = None, max_length = 255)


class TransactionUpdate(BaseModel):
    amount: float | None = None
    category: str | None = None
    name: str | None = None
    description: str | None = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    category: str
    name: str
    description: str | None

    class Config:
        from_attributes = True