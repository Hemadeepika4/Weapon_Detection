import sqlite3
from werkzeug.security import generate_password_hash

DB_NAME = 'weapon.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            original_path TEXT NOT NULL,
            output_path TEXT,
            detection_result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

def create_default_user():
    conn = get_db_connection()
    cursor = conn.cursor()

    email = 'admin@example.com'
    password = generate_password_hash('admin123')

    existing_user = cursor.execute(
        'SELECT * FROM users WHERE email = ?',
        (email,)
    ).fetchone()

    if not existing_user:
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            ('Admin', email, password)
        )
        conn.commit()

    conn.close()