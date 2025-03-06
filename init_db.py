import sqlite3
import os

def init_db():
    # The name of your SQLite file
    db_file = 'kysely.db'
    
    # Check if it exists
    db_exists = os.path.exists(db_file)

    # Connect (this creates the file if it doesn't already exist)
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Table 1: user responses to candlestick questions
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            image_name TEXT,
            expected_value REAL,
            confidence REAL,
            analysis_support TEXT,
            visual_clarity INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table 2: background questionnaire
    c.execute('''
        CREATE TABLE IF NOT EXISTS background_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            Age INTEGER,
            Gender TEXT,
            Education TEXT,
            InvestmentExperience INTEGER,
            FinMarkEngagement TEXT,
            AiEngagement TEXT,
            RiskTolerance INTEGER,
            FamiliarityAI INTEGER,
            KnowledgeGenAI INTEGER,
            AITrust INTEGER,
            DecisionConfidence INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table 3: consent records
    c.execute('''
        CREATE TABLE IF NOT EXISTS consent_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            consent BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

    # Print messages based on whether the DB was new or already existed
    if not db_exists:
        print(f"Database '{db_file}' did not exist and has been created.")
    else:
        print(f"Database '{db_file}' already exists. Ensured required tables are present.")

