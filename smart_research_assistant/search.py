import os
import json
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sentence_transformers import SentenceTransformer

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
db_url = os.getenv("TIDB_SQLALCHEMY_URL")
engine = create_engine(db_url)


def get_embedding(text):
    return model.encode(text).tolist()


def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def search_papers(query, top_k=3):
    q_emb = get_embedding(query)

    with engine.connect() as conn:
        rows = conn.exec_driver_sql(
            "SELECT id, title, content, embedding_json FROM research_papers"
        ).fetchall()

    results = []
    for row in rows:
        emb = json.loads(row[3])
        score = cosine_similarity(q_emb, emb)
        results.append((row[0], row[1], row[2], score))

    results = sorted(results, key=lambda x: x[3], reverse=True)
    return results[:top_k]
