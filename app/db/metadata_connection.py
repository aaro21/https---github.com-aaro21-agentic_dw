import os
from sqlalchemy import text, create_engine

metadata_engine = create_engine(os.getenv("METADATA_DB_URL"))

def get_source_connection_string(source_name: str) -> str | None:
    with metadata_engine.connect() as conn:
        row = conn.execute(
            text("SELECT ConnectionAlias FROM SourceSystems WHERE Name = :name AND IsActive = 1"),
            {"name": source_name}
        ).fetchone()
        if not row:
            return None
        alias = row[0]  # e.g., 'SOURCE_CRM_SQL_PROD_CONN'
        return os.getenv(alias)
