from fastapi import APIRouter
from sqlalchemy import text
from app.db.connection import get_engine

router = APIRouter(prefix="/sources", tags=["Sources"])

@router.get("/")
def list_sources():
    engine = get_engine("metadata")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM vw_SourceSystems")).fetchall()
        return [dict(row._mapping) for row in result]
