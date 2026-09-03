# 1. Connecting SQLite to Python
import sqlite3
from datetime import date

DB_NAME = "tracker.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# 2. Designing the tables (the schema)
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        # Table 1: Habits
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at DATE NOT NULL
            );
        """)

        # Table 2: Daily Completion Logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_date DATE NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE,
                UNIQUE(habit_id, completed_date)
            );
        """)

        conn.commit()


if __name__ == "__main__":
    init_db()
    print("Database and tables created successfully!")