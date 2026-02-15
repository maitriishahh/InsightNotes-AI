from database.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content_type TEXT,
        date_processed TEXT,
        duration INTEGER NOT NULL,
        transcript TEXT,
        structured_notes TEXT,
        youtube_id TEXT
    )
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_title
    ON notes(title)
    """)

    conn.commit()
    conn.close()