# Quick start

## 1. Backend
cd voice_assistant_system/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app:app --reload --port 8000

## 2. Web UI (React)
cd voice_assistant_system/voice_clients/web_assistant/react-voice-ui
npm install
npm start
Open http://localhost:3000

## 3. Python voice assistant (optional)
cd voice_assistant_system/voice_clients/python_assistant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python voice_assistant.py

## Notes
- Replace stubbed modules (detector, embedder, generate) with real models for production.
- Build FAISS index and SentenceTransformer models if using dense retriever.
- Configure integration endpoints (e-commerce, invoice) in backend/integrations.
