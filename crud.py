from sqlalchemy.orm import Session

from models import Transaction
from schemas import TransactionCreate, TransactionUpdate


# CREATE
def create_transaction(
    db: Session,
    transaction: TransactionCreate
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


# READ ALL
def get_transactions(db: Session):
    return db.query(Transaction).all()


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
def update_transaction(
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
    transaction.type = updated_transaction.type
    transaction.category = updated_transaction.category
    transaction.description = updated_transaction.description

    db.commit()
    db.refresh(transaction)

    return transaction


# PATCH
def patch_transaction(
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