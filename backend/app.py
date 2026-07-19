# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import chat_api, voice_api, face_api

app = FastAPI(title="Voice Assistant Backend")

# Allow local dev origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_api.router, prefix="/api/chat")
app.include_router(voice_api.router, prefix="/api/voice")
app.include_router(face_api.router, prefix="/api/face")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
