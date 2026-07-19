# backend/api/voice_api.py
from fastapi import APIRouter
from pydantic import BaseModel
from chatbot.chatbot import chat

router = APIRouter()

class VoiceRequest(BaseModel):
    user_id: str
    message: str

@router.post("/transcript")
async def transcript(req: VoiceRequest):
    # Accepts transcribed text from clients and returns assistant reply
    resp = chat(req.user_id, req.message)
    return {"response": resp}
