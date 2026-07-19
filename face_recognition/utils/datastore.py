# face_recognition/utils/datastore.py
import json, os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

DB_FILE = "face_recognition/embeddings/db.json"

def _load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def _save_db(db):
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

def enroll(name, embeddings_list):
    db = _load_db()
    mean = np.mean(embeddings_list, axis=0).tolist()
    db[name] = {"embedding": mean}
    _save_db(db)

def recognize(query_emb, threshold=0.6):
    db = _load_db()
    best = {"name": None, "score": -1}
    for name, data in db.items():
        emb = np.array(data["embedding"]).reshape(1, -1)
        score = cosine_similarity(emb, query_emb.reshape(1, -1))[0][0]
        if score > best["score"]:
            best = {"name": name, "score": float(score)}
    if best["score"] >= threshold:
        return best
    return {"name": "Unknown", "score": best["score"]}
