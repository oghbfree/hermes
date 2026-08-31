import sqlite3, json
from pathlib import Path
from datetime import datetime

db = Path.home() / '.hermes' / 'state.db'
conn = sqlite3.connect(str(db))
cur = conn.cursor()

# list tables
print("=== TABLES ===")
for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(r[0])

# inspect messages-like tables
for tbl in ['messages','telegram_messages','updates','channel_messages','sessions','memory','conversations']:
    try:
        print(f"\n=== {tbl} schema ===")
        for c in cur.execute(f"PRAGMA table_info({tbl})"):
            print(c)
    except Exception as e:
        print(f"{tbl}: {e}")
conn.close()