from database.db import get_connection
from datetime import datetime

def save_notes(title, content_type, duration, transcript, structured_notes, youtube_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
    INSERT INTO notes (title, content_type, date_processed, duration, transcript, structured_notes, youtube_id) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title,
            content_type,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            duration,
            transcript,
            structured_notes,
            youtube_id
            ))

        conn.commit()
        return cursor.lastrowid

def get_all_notes():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, title, content_type, date_processed
        FROM notes
        ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        

        return rows


def get_note_by_id(note_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT title, content_type, transcript, structured_notes, youtube_id
        FROM notes
        WHERE id = ?
        """, (note_id,))

        row = cursor.fetchone()

        if row is None:
            return None
        
        return row