import sqlite3, json, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

state_db = Path.home() / '.hermes' / 'state.db'
conn = sqlite3.connect(str(state_db))
cursor = conn.cursor()

# Check sessions table for telegram-related sessions
print("=== Sessions table structure ===")
cursor.execute("PRAGMA table_info(sessions)")
cols = cursor.fetchall()
print("Columns:", [c[1] for c in cols])

# Find sessions related to telegram topic 4
print("\n=== Looking for telegram sessions ===")
cursor.execute("SELECT * FROM sessions WHERE id LIKE '%telegram%' OR id LIKE '%topic%' OR id LIKE '%-1003784520976%' LIMIT 20")
rows = cursor.fetchall()
for row in rows:
    print(row[:5])  # Print first 5 columns

# Check if there's a session_id that matches the group/topic
print("\n=== All session IDs containing 'telegram' or '-1003784520976' ===")
cursor.execute("SELECT id FROM sessions WHERE id LIKE '%telegram%' OR id LIKE '%1003784520976%' LIMIT 20")
for row in cursor.fetchall():
    print(row[0])

conn.close()
