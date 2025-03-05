import sqlite3

def init_db():
    conn = sqlite3.connect('kysely.db')
    c = conn.cursor()

    # Create a table to store user responses
    # We'll keep it simple: id, user_identifier, image_name, expected_value, and a timestamp
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            image_name TEXT,
            expected_value REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized (or already exists).")
