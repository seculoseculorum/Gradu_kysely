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


    # Table 1: consent records
    c.execute('''
        CREATE TABLE IF NOT EXISTS consent_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            consent BOOLEAN,
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

    # Table 3: user responses to Task1 (candlestick questions)
    c.execute('''
        CREATE TABLE IF NOT EXISTS task1responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            image_name TEXT,
            user_estimate REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table 4: Task2 responses
    c.execute('''
        CREATE TABLE IF NOT EXISTS task2responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            image_name TEXT,
            user_estimate REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

    if not db_exists:
        print(f"Database '{db_file}' did not exist and has been created.")
    else:
        print(f"Database '{db_file}' already exists. Ensured required tables are present.")
