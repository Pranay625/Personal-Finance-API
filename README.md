A beginner-friendly Personal Finance REST API built with FastAPI, SQLAlchemy, and MySQL.

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

Install dependencies:

pip install -r requirements.txt

Configure environment variables:
Create a `.env` file (see `.env.example`):
- DATABASE_URL: MySQL connection string
- SECRET_KEY: JWT secret key

MySQL is installed separately and must be running.

Run database migrations:

alembic upgrade head

RUN:

uvicorn main:app --reload

API:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

ReDOC:

http://127.0.0.1:8000/redoc

Project Structure

fastapi/
├── alembic/              # Alembic database migration scripts
│   ├── versions/
│   └── env.py
├── routers/              # API sub-routers
│   ├── __init__.py
│   ├── finance.py        # Financial summaries and balance
│   └── transactions.py   # Transaction CRUD endpoints
├── __init__.py
├── alembic.ini           # Alembic configuration
├── auth.py               # JWT creation, verification, and get_current_user
├── crud.py               # Database CRUD operations (Users & Transactions)
├── db.py                 # SQLAlchemy engine and session setup
├── main.py               # FastAPI application entry point
├── models.py             # SQLAlchemy database models
├── schemas.py            # Pydantic request & response schemas
├── users.py              # User registration and authentication router
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
└── .gitignore            # Git ignore rules