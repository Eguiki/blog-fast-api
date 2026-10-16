from sqlalchemy import create_engine
from sqlalchemy.future import engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:erick@localhost:5433/dba"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
