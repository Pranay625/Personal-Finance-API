from fastapi import FastAPI

from db import Base, engine
from routers.transactions import router as transaction_router
from users import router as user_router


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(transaction_router)
app.include_router(user_router)
@app.get("/")
def home():
    return {
        "message": "Personal Finance API"
    }