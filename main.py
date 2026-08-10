from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models import Transaction
from schemas import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse
)


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Personal Finance API"}


# ---------------- CREATE ---------------- #

@app.post("/transactions", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):

    new_transaction = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        description=transaction.description
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


# ---------------- READ ALL ---------------- #

@app.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db)
):

    return db.query(Transaction).all()


# ---------------- READ ONE ---------------- #

@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):

    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


# ---------------- UPDATE ---------------- #

@app.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionCreate,
    db: Session = Depends(get_db)
):

    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transaction.amount = updated_transaction.amount
    transaction.type = updated_transaction.type
    transaction.category = updated_transaction.category
    transaction.description = updated_transaction.description

    db.commit()
    db.refresh(transaction)

    return transaction


# ---------------- PATCH ---------------- #

@app.patch("/transactions/{transaction_id}", response_model=TransactionResponse)
def patch_transaction(
    transaction_id: int,
    updated_transaction: TransactionUpdate,
    db: Session = Depends(get_db)
):

    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    data = updated_transaction.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)

    return transaction


# ---------------- DELETE ---------------- #

@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):

    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted successfully"}