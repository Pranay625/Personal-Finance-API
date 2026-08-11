from fastapi import FastAPI

from db import Base, engine
from routers.transactions import router as transaction_router

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(transaction_router)

@app.get("/")
def home():
    return {
        "message": "Personal Finance API"
    }