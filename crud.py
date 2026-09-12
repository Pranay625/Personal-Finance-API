from sqlalchemy.orm import Session
from models import Transaction, User
from schemas import TransactionCreate, TransactionUpdate, UserCreate

import bcrypt


# CREATE
def create_transaction(
    db: Session,
    transaction: TransactionCreate,
    user_id: int
):
    new_transaction = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        category_id=transaction.category_id,
        name=transaction.name,
        description=transaction.description,
        transaction_date=transaction.transaction_date,
        user_id=user_id
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


# READ ALL
def get_transactions(
    db: Session,
    user_id: int,
    category_id: int | None = None,
    transaction_type: str | None = None,
    name: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    start_date=None,
    end_date=None,
    skip: int = 0,
    limit: int = 10,
    sort: str | None = None
):
    query = db.query(Transaction).filter(
        Transaction.user_id == user_id
    )

    if category_id is not None:
        query = query.filter(
            Transaction.category_id == category_id
        )

    if transaction_type:
        query = query.filter(
            Transaction.type == transaction_type
        )

    if name:
        query = query.filter(
            Transaction.name == name
        )

    if min_amount is not None:
        query = query.filter(
            Transaction.amount >= min_amount
        )

    if max_amount is not None:
        query = query.filter(
            Transaction.amount <= max_amount
        )

    if start_date is not None:
        query = query.filter(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:
        query = query.filter(
            Transaction.transaction_date <= end_date
        )

    if sort == "amount":
        query = query.order_by(
            Transaction.amount.asc()
        )

    elif sort == "-amount":
        query = query.order_by(
            Transaction.amount.desc()
        )

    return query.offset(skip).limit(limit).all()


# READ ONE
def get_transaction(
    db: Session,
    transaction_id: int,
    user_id: int
):
    return (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
        .first()
    )


# UPDATE
def update_full(
    db: Session,
    transaction_id: int,
    updated_transaction: TransactionCreate,
    user_id: int
):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
        .first()
    )

    if not transaction:
        return None

    transaction.amount = updated_transaction.amount
    transaction.type = updated_transaction.type
    transaction.category_id = updated_transaction.category_id
    transaction.name = updated_transaction.name
    transaction.description = updated_transaction.description
    transaction.transaction_date = updated_transaction.transaction_date

    db.commit()
    db.refresh(transaction)

    return transaction


# PATCH
def update_partial(
    db: Session,
    transaction_id: int,
    updated_transaction: TransactionUpdate,
    user_id: int
):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
        .first()
    )

    if not transaction:
        return None

    data = updated_transaction.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)

    return transaction


# DELETE
def delete_transaction(
    db: Session,
    transaction_id: int,
    user_id: int
):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
        .first()
    )

    if not transaction:
        return None

    db.delete(transaction)
    db.commit()

    return transaction