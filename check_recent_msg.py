import json, urllib.request, sys
from pathlib import Path

env_path = Path.home() / '.hermes' / '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if 'TELEGRAM_BOT_TOKEN=' in line:
            token = line[len('TELEGRAM_BOT_TOKEN='):].strip()
            break

if not token:
    print('ERROR: No token')
    sys.exit(1)

# Try to get recent messages by sending a getMessage with a recent message_id
# First, let's try sending a test to see if the bot can access topic messages
# The Telegram API doesn't have a "get chat history" for bots by default
# But let's try getChatMember to verify bot is in the group

chat_id = '-1003784520976'
url = 'https://api.telegram.org/bot' + token + '/getChatMember'
payload = json.dumps({'chat_id': chat_id, 'user_id': 8277244378}).encode('utf-8')
req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req, timeout=15) as resp:
    result = json.loads(resp.read().decode('utf-8'))
print('Bot membership:')
print(json.dumps(result, indent=2, ensure_ascii=False)[:500])

# Check if there's a state.db or message queue we can query
print('\n\n--- Checking state.db for telegram messages ---')
state_db = Path.home() / '.hermes' / 'state.db'
if state_db.exists():
    print('state.db exists, size:', state_db.stat().st_size)
    # Try to query it
    import sqlite3
    try:
        conn = sqlite3.connect(str(state_db))
        cursor = conn.cursor()
        # List tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print('Tables:', [t[0] for t in tables])
        
        # Look for telegram-related tables
        for t in tables:
            tname = t[0]
            if 'telegram' in tname.lower() or 'message' in tname.lower() or 'channel' in tname.lower():
                print(f'\nTable: {tname}')
                cursor.execute(f"PRAGMA table_info({tname})")
                cols = cursor.fetchall()
                print('  Columns:', [c[1] for c in cols])
                cursor.execute(f"SELECT COUNT(*) FROM {tname}")
                count = cursor.fetchone()[0]
                print(f'  Row count: {count}')
    except Exception as e:
        print('DB error:', str(e))
    finally:
        conn.close()
else:
    print('state.db not found')
