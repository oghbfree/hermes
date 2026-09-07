import sqlite3, os
from pathlib import Path
state_db = Path.home() / '.hermes' / 'state.db'
conn = sqlite3.connect(str(state_db))
conn.row_factory = sqlite3.Row
c = conn.cursor()
print("=== tables ===")
for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(r['name'])
print("\n=== messages schema ===")
for r in c.execute("PRAGMA table_info(messages)"):
    print([r[k] for k in r.keys()])
print("\n=== latest 25 messages (any) ===")
try:
    rows = c.execute("SELECT id, session_id, role, content, platform_message_id, timestamp FROM messages ORDER BY timestamp DESC LIMIT 25").fetchall()
    for row in rows:
        cp = (row['content'][:180].replace('\n',' ')) if row['content'] else ''
        print(f"#{row['id']} plat={row['platform_message_id']} role={row['role']} ts={row['timestamp']} sess={(row['session_id'] or '')[:40]}")
        print(f"   {cp}")
except Exception as e:
    print("ERR", e)
conn.close()