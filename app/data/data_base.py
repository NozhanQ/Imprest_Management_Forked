import sqlite3
from pathlib import Path
from datetime import datetime
import uuid

DB_PATH = Path(__file__).parent / "app.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS records
                    (
                        id
                        TEXT
                        PRIMARY
                        KEY,
                        title
                        TEXT
                        NOT
                        NULL,
                        description
                        TEXT,
                        amount
                        REAL,
                        record_date
                        TEXT,
                        image_path
                        TEXT,
                        last_modified
                        TEXT
                        NOT
                        NULL,
                        source_pc
                        TEXT
                        NOT
                        NULL,
                        deleted
                        INTEGER
                        DEFAULT
                        0
                    ) """)
    conn.commit()
    conn.close()


def insert_record(title, description, amount, record_date, image_path, source_pc, expense_center, expense_type,company_name):
    conn = get_connection()
    cur = conn.cursor()

    record_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    cur.execute("""
    INSERT INTO records (
        id, title, description, amount,
        record_date, image_path,
        last_modified, source_pc, expense_center, expense_type, company_name
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? , ? , ? )
    """, (
        record_id,
        title,
        description,
        amount,
        record_date,
        image_path,
        now,
        source_pc,
        expense_center,
        expense_type,
        company_name
    ))

    conn.commit()
    conn.close()


def get_all_records():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM records WHERE deleted = 0")
    rows = cur.fetchall()

    conn.close()
    return rows
