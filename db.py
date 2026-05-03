import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        result TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_message(message, result):
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO logs (message, result, timestamp)
    VALUES (?, ?, ?)
    """, (message, result, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

# 👇 NEW FUNCTION (for viewing DB)
def view_db():
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()

    c.execute("SELECT * FROM logs")
    rows = c.fetchall()

    if len(rows) == 0:
        print("Database is empty.")
    else:
        for row in rows:
            print(row)

    conn.close()


# 👇 This makes `python db.py` work
if __name__ == "__main__":
    view_db()