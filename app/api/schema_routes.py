from fastapi import APIRouter
from app.services.schema_explorer import list_tables, list_columns

router = APIRouter(prefix="/schema", tags=["Schema"])

@router.get("/tables")
def get_tables():
    return list_tables()

@router.get("/tables/{table_name}/columns")
def get_columns(table_name: str):
    return list_columns(table_name)
