import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sentence_transformers import SentenceTransformer

load_dotenv()

# Load model + DB
model = SentenceTransformer("all-MiniLM-L6-v2")
db_url = os.getenv("TIDB_SQLALCHEMY_URL")
engine = create_engine(db_url)


def get_embedding(text_str):
    return model.encode(text_str).tolist()


def insert_text(title, content):
    embedding = get_embedding(content)
    embedding_json = json.dumps(embedding)

    conn = engine.raw_connection()
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO research_papers (title, content, embedding_json)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (title, content, embedding_json))
        conn.commit()
        print(f"Inserted: {title}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    samples = [
        (
            "AI Research",
            "Artificial intelligence is transforming healthcare and education.",
        ),
        ("Databases", "TiDB is a distributed SQL database with vector search support."),
        (
            "NLP Models",
            "Sentence Transformers are great for semantic similarity tasks.",
        ),
        ("Machine Learning", "Machine learning allows computers to learn from data."),
        (
            "Deep Learning",
            "Deep learning uses neural networks to model complex patterns.",
        ),
        (
            "Reinforcement Learning",
            "Reinforcement learning teaches agents via rewards.",
        ),
        (
            "Computer Vision",
            "AI in computer vision enables image recognition and object detection.",
        ),
        (
            "Healthcare AI",
            "AI assists in medical imaging, diagnosis, and drug discovery.",
        ),
        ("Education AI", "AI can personalize learning experiences for students."),
        (
            "Cloud Databases",
            "Distributed cloud databases scale horizontally and support vector search.",
        ),
    ]

    for title, content in samples:
        insert_text(title, content)
