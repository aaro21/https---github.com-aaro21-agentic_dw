from fastapi import FastAPI
from app.api import schema_routes, chat_routes

app = FastAPI(title="Agentic DW")

app.include_router(schema_routes.router)
app.include_router(chat_routes.router)
