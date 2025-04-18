import sqlite3
import pandas as pd
from pathlib import Path

# Connect to the database.
conn = sqlite3.connect('salainentietokanta.db')

# Where to save the CSVs (current working directory by default).
# Feel free to change this to any folder Path("some/other/dir")
output_dir = f"{Path.cwd()}//answerdata//"

# List of table names to display and export.
tables = ["task1responses", "background_responses",
          "consent_responses", "task2responses"]

for table in tables:
    # Fetch the whole table into a DataFrame.
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    
    # Print to console for a quick look.
    print(f"--- {table} ---")
    print(df, "\n")
    
    # Write to CSV (table_name.csv) with no row index column.
    csv_path = f"{output_dir}//{table}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved → {csv_path}")

conn.close()
