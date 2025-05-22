import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.metadata_connection import get_source_connection_string

# For named core layers
def get_engine(layer: str):
    db_urls = {
        "stage": os.getenv("STAGE_DB_URL"),
        "bronze": os.getenv("BRONZE_DB_URL"),
        "silver": os.getenv("SILVER_DB_URL"),
        "gold": os.getenv("GOLD_DB_URL"),
        "metadata": os.getenv("METADATA_DB_URL"),
    }
    if layer not in db_urls or not db_urls[layer]:
        raise ValueError(f"No DB URL configured for: {layer}")
    return create_engine(db_urls[layer])

# For dynamic source (SQL Server, Oracle, etc.)
def get_source_engine(source_name: str):
    conn_str = get_source_connection_string(source_name)
    if not conn_str:
        raise ValueError(f"No connection string found for source: {source_name}")
    return create_engine(conn_str)
