# backend/api/face_api.py
from fastapi import APIRouter, File, UploadFile
from typing import List, Dict
from utils import detector, embedder, datastore  # local modules in face_recognition/utils

router = APIRouter()

@router.post("/recognize")
async def recognize_image(image: UploadFile = File(...)):
    # read image bytes and run detection + recognition
    from PIL import Image
    img = Image.open(image.file).convert("RGB")
    faces = detector.detect_align(img)  # returns list of PIL faces and boxes
    results = []
    for face, box in faces:
        emb = embedder.get_embedding(face)
        res = datastore.recognize(emb)
        results.append({"box": box, "name": res["name"], "score": res["score"]})
    return {"faces": results}
