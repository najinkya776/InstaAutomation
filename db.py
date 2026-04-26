import sqlite3
from contextlib import contextmanager

DB_PATH = "posted.db"


@contextmanager
def _conn():
    con = sqlite3.connect(DB_PATH)
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db():
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS posted (
                pk          TEXT PRIMARY KEY,
                hashtag     TEXT,
                original_url TEXT,
                posted_at   DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS run_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                status      TEXT,
                message     TEXT
            )
        """)


def already_posted(reel_pk: str) -> bool:
    with _conn() as con:
        row = con.execute(
            "SELECT 1 FROM posted WHERE pk = ?", (str(reel_pk),)
        ).fetchone()
        return row is not None


def mark_posted(reel_pk: str, hashtag: str = "", original_url: str = ""):
    with _conn() as con:
        con.execute(
            "INSERT OR IGNORE INTO posted (pk, hashtag, original_url) VALUES (?, ?, ?)",
            (str(reel_pk), hashtag, original_url),
        )


def log_run(status: str, message: str):
    with _conn() as con:
        con.execute(
            "INSERT INTO run_log (status, message) VALUES (?, ?)",
            (status, message),
        )
