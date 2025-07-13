import os
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load env variables
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")


RAW_DATA_DIR = "data/raw/telegram_messages"


def connect():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME
    )
    conn.autocommit = True
    return conn


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE SCHEMA IF NOT EXISTS raw;

            CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                id INTEGER,
                date TIMESTAMP,
                message TEXT,
                sender_id TEXT,
                has_media BOOLEAN,
                media_file TEXT,
                channel_name TEXT,
                load_date DATE
            );
        """
        )


def load_data(conn):
    all_rows = []
    for date_folder in os.listdir(RAW_DATA_DIR):
        date_path = os.path.join(RAW_DATA_DIR, date_folder)
        if not os.path.isdir(date_path):
            continue
        for file in os.listdir(date_path):
            if file.endswith(".json"):
                channel_name = file.replace(".json", "")
                file_path = os.path.join(date_path, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    messages = json.load(f)
                    for msg in messages:
                        row = (
                            msg.get("id"),
                            msg.get("date"),
                            msg.get("message"),
                            msg.get("sender_id"),
                            msg.get("has_media"),
                            msg.get("media_file"),
                            channel_name,
                            date_folder,
                        )
                        all_rows.append(row)

    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO raw.telegram_messages
            (id, date, message, sender_id, has_media, media_file,
            channel_name, load_date)
            VALUES %s
            """,
            all_rows,
        )
    print(f"Inserted {len(all_rows)} rows into raw.telegram_messages")


if __name__ == "__main__":
    conn = connect()
    create_table(conn)
    load_data(conn)
    conn.close()
