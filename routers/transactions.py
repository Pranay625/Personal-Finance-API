from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud

from db import get_db
from schemas import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse
)


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


# ---------------- CREATE ---------------- #

@router.post("/", response_model=TransactionResponse, status_code = 201)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)

):
    return crud.create_transaction(
        db, 
        transaction)


# ---------------- READ ALL ---------------- #

@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    category: str | None =None,
    name: str | None = None,
    min_amount: int | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return crud.get_transactions(
        db,
        category,
        name,
        min_amount,
        skip,
        limit
    )


# ---------------- READ ONE ---------------- #

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = crud.get_transaction(
        db,
        transaction_id
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


# ---------------- UPDATE ---------------- #

@router.put(
    "/{transaction_id}",
    response_model=TransactionResponse
)
def update_full(
    transaction_id: int,
    updated_transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    transaction = crud.update_transaction(
        db,
        transaction_id,
        updated_transaction
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )
    return transaction


# ---------------- PATCH ---------------- #

@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse
)
def update_partial(
    transaction_id: int,
    updated_transaction: TransactionUpdate,
    db: Session = Depends(get_db)
):
    transaction = crud.patch_transaction(
        db,
        transaction_id,
        updated_transaction
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


# ---------------- DELETE ---------------- #

@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = crud.delete_transaction(
        db,
        transaction_id
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {
        "message": "Transaction deleted successfully"
    }