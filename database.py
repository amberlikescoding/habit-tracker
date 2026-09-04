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

def add_habit(name: str):
    today = date.today().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO habits (name, created_at) VALUES (?, ?);",
            (name, today)
        )
        conn.commit()
        return cursor.lastrowid

def fetch_every_habit_with_today_status():
    today = date.today().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT
                h.id,
                h.name,
                h.created_at,
                CASE WHEN c.id IS NOT NULL THEN 1 ELSE 0 END AS completed_today
            FROM habits h
            LEFT JOIN completions c
                ON h.id = c.habit_id AND c.completed_date = ?
            ORDER BY h.id DESC;
        """
        cursor.execute(query, (today,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()

    new_id = add_habit("Drink 2L of water everyday :)")
    print(f"Added habit with ID = {new_id}")

    all_habits = fetch_every_habit_with_today_status()
    print("All habits in DB: ")
    print(all_habits)
