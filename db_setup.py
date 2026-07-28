import sqlite3

def create_table():
    connct = sqlite3.connect("tasks.db")
    cursor = connct.cursor()
   
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks(" \
    "task_id INTEGER PRIMARY KEY," \
    "title TEXT NOT NULL," \
    "description TEXT," \
    "created_at TEXT DEFAULT CURRENT_TIMESTAMP," \
    "enddate NUMERIC," \
    "streak INTEGER DEFAULT 0)")
    connct.commit()
    connct.close()