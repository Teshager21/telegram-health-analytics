import os
import psycopg2
import pytest
from dotenv import load_dotenv

load_dotenv(override=True)
print(os.getenv("DB_PASSWORD"))

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")


@pytest.fixture(scope="module")
def db_conn():
    """Fixture to open and close DB connection for tests."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
    )
    conn.autocommit = True
    yield conn
    conn.close()


def test_table_exists(db_conn):
    with db_conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'raw'
            AND table_name = 'telegram_messages';
        """
        )
        result = cur.fetchone()
        assert result is not None, "Table raw.telegram_messages does not exist."


def test_table_not_empty(db_conn):
    with db_conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*) FROM raw.telegram_messages;
        """
        )
        count = cur.fetchone()[0]
        assert count > 0, "Table raw.telegram_messages is empty."


def test_select_sample_rows(db_conn):
    with db_conn.cursor() as cur:
        cur.execute(
            """
            SELECT *
            FROM raw.telegram_messages
            LIMIT 5;
        """
        )
        rows = cur.fetchall()
        assert rows is not None, "SELECT query returned None."
        assert len(rows) > 0, "No rows returned from telegram_messages."
        for row in rows:
            print(row)
