from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from enum import Enum

import crud

from auth import get_current_user
from db import get_db
from models import User, Category
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
    category = db.query(Category).filter(
        Category.id == transaction.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=400,
            detail=f"Category with id {transaction.category_id} not found"
        )

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
    category_id: int | None = Query(
        default=None,
        gt=0
    ),

    transaction_type: str | None = None,

    name: str | None = None,

    min_amount: float | None = Query(
        default=None,
        ge=0
    ),

    max_amount: float | None = Query(
        default=None,
        ge=0
    ),

    start_date: date | None = None,

    end_date: date | None = None,

    skip: int = Query(
        default=0,
        ge=0
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),

    sort: SortOrder | None = None,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):
    # Validate date range
    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be later than end_date"
        )

    # Validate amount range
    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):
        raise HTTPException(
            status_code=400,
            detail="min_amount cannot be greater than max_amount"
        )

    return crud.get_transactions(
        db=db,
        user_id=current_user.id,
        category_id=category_id,
        transaction_type=transaction_type,
        name=name,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date,
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
    category = db.query(Category).filter(
        Category.id == updated_transaction.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=400,
            detail=f"Category with id {updated_transaction.category_id} not found"
        )

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
    if updated_transaction.category_id is not None:
        category = db.query(Category).filter(
            Category.id == updated_transaction.category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=400,
                detail=f"Category with id {updated_transaction.category_id} not found"
            )

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