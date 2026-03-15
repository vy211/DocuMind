import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "192.168.0.13"),
        database=os.getenv("POSTGRES_DB", "devdb"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "admin123"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Create tables here if needed
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
