import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQL_SERVER_URL = os.getenv("SQL_SERVER_URL")

engine = create_engine(SQL_SERVER_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
