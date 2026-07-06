import sqlite3, json, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

state_db = Path.home() / '.hermes' / 'state.db'
conn = sqlite3.connect(str(state_db))
cursor = conn.cursor()

# Check messages with platform_message_id (telegram messages should have this)
print("=== Messages with non-null platform_message_id ===")
cursor.execute("SELECT COUNT(*) FROM messages WHERE platform_message_id IS NOT NULL")
print("Count:", cursor.fetchone()[0])

# Get the most recent messages with platform_message_id
print("\n=== Most recent messages with platform_message_id ===")
cursor.execute("""
    SELECT id, session_id, role, content, platform_message_id, timestamp 
    FROM messages 
    WHERE platform_message_id IS NOT NULL 
    ORDER BY timestamp DESC 
    LIMIT 20
""")
rows = cursor.fetchall()
for row in rows:
    msg_id, session_id, role, content, plat_id, ts = row
    content_preview = (content[:100] + '...') if content and len(content) > 100 else (content or '')
    print(f"plat_id={plat_id} | role={role} | session={session_id[:30] if session_id else ''} | ts={ts}")
    print(f"  content: {content_preview}")
    print()

# Also check for messages containing 'telegram' or group id
print("\n=== Messages containing 'telegram' or group ID ===")
cursor.execute("""
    SELECT id, session_id, role, content, platform_message_id, timestamp 
    FROM messages 
    WHERE content LIKE '%telegram%' OR content LIKE '%-1003784520976%' OR content LIKE '%topic%4%'
    ORDER BY timestamp DESC 
    LIMIT 10
""")
rows = cursor.fetchall()
print(f"Found {len(rows)} messages")
for row in rows:
    msg_id, session_id, role, content, plat_id, ts = row
    content_preview = (content[:150] + '...') if content and len(content) > 150 else (content or '')
    print(f"  plat_id={plat_id} | role={role} | ts={ts}")
    print(f"  content: {content_preview}")
    print()

conn.close()
