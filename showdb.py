import sqlite3
import pandas as pd

# Connect to the database.
conn = sqlite3.connect('kysely.db')

# List of table names to display.
tables = ["task1responses", "background_responses", "consent_responses", "task2responses"]

# Loop over each table, fetch the data as a DataFrame, and print it.
for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    print(f"--- {table} ---")
    print(df)
    print("\n")

conn.close()
