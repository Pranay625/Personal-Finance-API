from sqlalchemy.orm import Session

from models import Transaction
from schemas import TransactionCreate, TransactionUpdate
from enum import Enum

# CREATE
def create_transaction(
    db: Session,
    transaction: TransactionCreate
):
    new_transaction = Transaction(
        amount=transaction.amount,
        category=transaction.category,
        name=transaction.name,
        description=transaction.description
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


# READ ALL
def get_transactions(
    db,
    category = None,
    name = None,
    min_amount = None,
    skip = 0,
    limit = 10,
    sort = None
):
    query = db.query(Transaction)

    if category: 
        query = query.filter(Transaction.category == category)

    if name: 
        query = query.filter(Transaction.name == name)

    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)

    if sort == "amount":
        query = query.order_by(Transaction.amount.asc())

    elif sort == "-amount":
        query = query.order_by(Transaction.amount.desc())
        
    return query.offset(skip).limit(limit).all()


# READ ONE
def get_transaction(
    db: Session,
    transaction_id: int
):
    return (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )


# UPDATE
def update_full(
    db: Session,
    transaction_id: int,
    updated_transaction: TransactionCreate
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        return None

    transaction.amount = updated_transaction.amount
    transaction.category = updated_transaction.category
    transaction.name=     updated_transaction.name
    transaction.description = updated_transaction.description

    db.commit()
    db.refresh(transaction)

    return transaction


# PATCH
def update_partial(
    db: Session,
    transaction_id: int,
    updated_transaction: TransactionUpdate
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        return None

    data = updated_transaction.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)

    return transaction


# DELETE
def delete_transaction(
    db: Session,
    transaction_id: int
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        return None

    db.delete(transaction)
    db.commit()

    return transaction