from pydantic import BaseModel


class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    description: str


class TransactionUpdate(BaseModel):
    amount: float | None = None
    type: str | None = None
    category: str | None = None
    description: str | None = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    description: str

    class Config:
        from_attributes = True