import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

db_url = os.getenv("TIDB_SQLALCHEMY_URL")
engine = create_engine(db_url)


def init_db():
    sql = """
    CREATE TABLE IF NOT EXISTS research_papers (
        id BIGINT PRIMARY KEY AUTO_RANDOM,
        title VARCHAR(255),
        content TEXT,
        embedding_json JSON
    );
    """
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print("research_papers table ready.")


if __name__ == "__main__":
    init_db()
