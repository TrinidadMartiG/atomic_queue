"""
Dev utility: verify database connectivity.

Run once to confirm the DB is reachable before applying migrations.
Migrations are applied separately and explicitly via SQL files in db/migrations/.
"""
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


if __name__ == "__main__":
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0].split(",")[0]
        conn.close()
        print(f"Connected: {version}")
        print("Run migrations manually: psql -f db/migrations/001_create_tasks.sql")
    except Exception as e:
        print(f"Connection failed: {e}")
