# backend/api/chat_api.py
from fastapi import APIRouter
from pydantic import BaseModel
from chatbot.chatbot import chat

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@router.post("/message")
async def message(req: ChatRequest):
    resp = chat(req.user_id, req.message)
    return {"response": resp}
