import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import  DeclarativeBase

load_dotenv()

DB_URL = os.getenv("TEST_DB_URL")
if not DB_URL:
    raise ValueError("TEST_DB_URL is not set")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

class Base(DeclarativeBase):
    pass