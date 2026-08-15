A beginner-friendly Personal Finance REST API built with FastAPI, SQLAlchemy, and MySQL

TECH STACK:

Python 3.12
FastAPI
Uvicorn
SQLAlchemy
PyMySQL
MySQL
Pydantic
bcrypt
Swagger/OpenAPI

Installation

Create and activate the virtual environment:

python -m venv venv
venv\Scripts\activate

Install everything used so far:

pip install fastapi uvicorn sqlalchemy pymysql bcrypt

MySQL is installed separately and must be running.

RUN:

uvicorn main:app --reload

API:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

ReDOC:

http://127.0.0.1.8000/redoc

Project Structure

fastapi/
├── main.py
├── db.py
├── models.py
├── schemas.py
├── crud.py
├── transactions.py
├── users.py
└── venv/