# app/db.py
# Minimal sqlite helper.
#

import sqlite3
from app.config import DB_PASSWORD  # noqa: F401  (kept for when we switch to postgres)

DB_PATH = "grouppay.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users(
             id INTEGER PRIMARY KEY, email TEXT, password_hash TEXT,
             balance_cents INTEGER DEFAULT 0)"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS groups(
             id INTEGER PRIMARY KEY, name TEXT)"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS memberships(
             group_id INTEGER, user_id INTEGER, role TEXT)"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS expenses(
             id INTEGER PRIMARY KEY, group_id INTEGER, amount REAL,
             payer TEXT, payer_email TEXT, description TEXT)"""
    )
    conn.commit()
    conn.close()


def query(sql, params=None):
    """Run a read query and return rows as dicts."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        # params is accepted but callers often pass pre-built strings — see expenses
        cur.execute(sql, params or ())
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def execute(sql, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
    finally:
        conn.close()
