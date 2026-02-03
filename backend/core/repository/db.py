import os
import sqlite3
import logging
from mysql.connector.pooling import MySQLConnectionPool
import bcrypt
import threading

logger = logging.getLogger(__name__)

_db_pool = None
_lock = threading.Lock()

def is_sqlite():
    return os.getenv("DB_TYPE", "sqlite").lower() == "sqlite"

def init_sqlite_db():
    db_path = os.getenv("SQLITE_DB_PATH", "tickets.db")
    dir_name = os.path.dirname(db_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    if not os.path.exists(db_path):
        logger.info(f"Creating SQLite database at {db_path}")
        conn = sqlite3.connect(db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_type TEXT NOT NULL,
                impact INTEGER NOT NULL,
                customer_type TEXT NOT NULL,
                created_at TEXT NOT NULL,
                priority_score INTEGER NOT NULL,
                priority_level TEXT NOT NULL
            )
        """)

        demo_hash = bcrypt.hashpw(b"password", bcrypt.gensalt()).decode()
        cur.execute("""
            INSERT OR IGNORE INTO users (username, password_hash)
            VALUES (?, ?)
        """, ("vineel", demo_hash))

        conn.commit()
        conn.close()
        logger.info("SQLite DB initialized")

def get_connection():
    global _db_pool
    if is_sqlite():
        init_sqlite_db()
        db_path = os.getenv("SQLITE_DB_PATH", "tickets.db")
        conn = sqlite3.connect(db_path, timeout=10.0, check_same_thread=True)
        conn.row_factory = sqlite3.Row
        return conn

    if _db_pool is None:
        with _lock:
            if _db_pool is None:
                _db_pool = MySQLConnectionPool(
                    pool_name="ticket_pool",
                    pool_size=int(os.getenv("MYSQL_POOL_SIZE", 5)),
                    pool_reset_session=True,
                    host=os.getenv("DB_HOST", "localhost"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME"),
                    port=int(os.getenv("DB_PORT", 3306)),
                )
    return _db_pool.get_connection()