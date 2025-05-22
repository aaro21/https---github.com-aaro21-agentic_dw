from fastapi import APIRouter
from pydantic import BaseModel
from app.services.langchain_agent import agent

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str

@router.post("/")
def ask_agent(request: ChatRequest):
    response = agent.run(request.query)
    return {"response": response}
