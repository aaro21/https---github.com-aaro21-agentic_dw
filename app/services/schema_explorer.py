from sqlalchemy import inspect
from app.db.connection import engine

def list_tables():
    inspector = inspect(engine)
    return inspector.get_table_names()

def list_columns(table_name: str):
    inspector = inspect(engine)
    return inspector.get_columns(table_name)
