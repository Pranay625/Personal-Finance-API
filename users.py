from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import crud

from db import get_db
from schemas import UserCreate, UserResponse, UserLogin

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post(
    "/",
    response_model = UserResponse,
    status_code = 201
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)

):
    try:
        return crud.create_user(db, user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code = 409,
            detail = "Username already exists."
        )

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    authenticated_user = crud.authenticate_user(
        db,
        user.username,
        user.password
    )

    if not authenticated_user:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid username or password."
        )

    return {
        "message": "Login successful",
        "username": authenticated_user.username
    }