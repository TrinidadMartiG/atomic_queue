import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


try:
    # Connect to the PostgreSQL server
    conn = psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("Connection successful!")

    # Perform database operations using a cursor
    with conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Connected to PostgreSQL version: {db_version}")

    # Commit changes (if any) and close the connection
    conn.commit()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
