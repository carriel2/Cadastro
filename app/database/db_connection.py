import psycopg2
from app.database.db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn
