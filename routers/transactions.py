from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from enum import Enum

import crud

from auth import get_current_user
from db import get_db
from models import User
from schemas import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse
)


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


class SortOrder(str, Enum):
    LOW_TO_HIGH = "amount"
    HIGH_TO_LOW = "-amount"


# ---------------- CREATE ---------------- #

@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=201
)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_transaction(
        db,
        transaction,
        current_user.id
    )


# ---------------- READ ALL ---------------- #

@router.get(
    "/",
    response_model=list[TransactionResponse]
)
def get_transactions(
    category_id: int | None = None,
    transaction_type: str | None = None,
    name: str | None = None,
    min_amount: float | None = None,
    skip: int = 0,
    limit: int = 10,
    sort: SortOrder | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_transactions(
        db=db,
        user_id=current_user.id,
        category_id=category_id,
        transaction_type=transaction_type,
        name=name,
        min_amount=min_amount,
        skip=skip,
        limit=limit,
        sort=sort
    )


# ---------------- READ ONE ---------------- #

@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = crud.get_transaction(
        db,
        transaction_id,
        current_user.id
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = crud.update_full(
        db,
        transaction_id,
        updated_transaction,
        current_user.id
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = crud.update_partial(
        db,
        transaction_id,
        updated_transaction,
        current_user.id
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


# ---------------- DELETE ---------------- #

@router.delete(
    "/{transaction_id}"
)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = crud.delete_transaction(
        db,
        transaction_id,
        current_user.id
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {
        "message": "Transaction deleted successfully"
    }