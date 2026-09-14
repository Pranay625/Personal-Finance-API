from fastapi import FastAPI

from routers.transactions import router as transaction_router
from routers.finance import router as finance_router
from users import router as user_router


app = FastAPI(
    title="Personal Finance API",
    description="Backend API for managing personal finances and transactions.",
    version="1.0.0"
)


app.include_router(transaction_router)
app.include_router(finance_router)
app.include_router(user_router)


@app.get("/")
def home():
    return {
        "message": "Personal Finance API"
    }