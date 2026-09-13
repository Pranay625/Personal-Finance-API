from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from auth import get_current_user
from db import get_db
from models import User, Transaction
from schemas import FinanceSummary


router = APIRouter(
    prefix="/finance",
    tags=["Finance"]
)


@router.get(
    "/summary",
    response_model=FinanceSummary
)
def get_finance_summary(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(
        func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.type == "income",
                        Transaction.amount
                    ),
                    else_=0
                )
            ),
            0
        ).label("total_income"),

        func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.type == "expense",
                        Transaction.amount
                    ),
                    else_=0
                )
            ),
            0
        ).label("total_expenses")
    ).filter(
        Transaction.user_id == current_user.id
    )

    if start_date is not None:
        query = query.filter(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:
        query = query.filter(
            Transaction.transaction_date <= end_date
        )

    result = query.first()

    total_income = Decimal(result.total_income)
    total_expenses = Decimal(result.total_expenses)

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": total_income - total_expenses
    }