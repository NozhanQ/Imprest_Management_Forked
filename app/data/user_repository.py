from app.data.data_base import insert_record
import sqlite3


def save_data(data: dict):
    insert_record(
        title=data["title"],
        explanation=data["explanation"],
        amount=float(data["amount"]),
        record_date=data["record_date"],
        image_path=data["image_path"],
        source_pc=data["source_pc"],
        expense_center=data["expense_center"],
        expense_type=data["expense_type"],
        company_name=data["company_name"]
    )


class load_data():
    DB_PATH = "app/data/app.db"

    @staticmethod
    def get_connection():
        return sqlite3.connect(load_data.DB_PATH)

    @staticmethod
    def fetch_all(query, params=()):
        conn = load_data.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return rows
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_invoices_by_title(text):
        query = """
            SELECT title, explanation, record_date, amount, expense_center,expense_type,company_name
            FROM records
            WHERE title LIKE ?
        """
        return load_data.fetch_all(query, (f"%{text}%",))

    @staticmethod
    def get_invoices_by_registration_date(date_str):
        query = """
            SELECT title, explanation, record_date, amount, expense_center,expense_type,company_name
            FROM records
            WHERE record_date >= ? \
              AND record_date < ?
            ORDER BY record_date DESC \
            """
        start = f"{date_str}T00:00:00"
        end = f"{date_str}T23:59:59.999999"
        return load_data.fetch_all(query, (start, end))

    @staticmethod
    def get_invoices_by_login_date(date_str):
        query = """
            SELECT title, explanation, record_date, amount, expense_center,expense_type,company_name
            FROM records
            WHERE last_modified LIKE ?
            ORDER BY last_modified DESC \
            """
        return load_data.fetch_all(query, (f"{date_str}%",))

    @staticmethod
    def get_invoices_by_explanation(text):
        query = """
            SELECT title, explanation, record_date, amount, expense_center,expense_type,company_name
            FROM records
            WHERE explanation LIKE ?
        """
        return load_data.fetch_all(query, (f"%{text}%",))
