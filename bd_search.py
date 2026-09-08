import sqlite3, datetime, os
db = sqlite3.connect(r'C:/Users/User/AppData/Local/hermes/state.db')
cur = db.cursor()

# 1) Recent sessions overall
print("=== Sessions since 2026-08-24 ===")
since = int(datetime.datetime(2026,8,24,0,0).timestamp())
cur.execute('SELECT id,title,started_at,message_count,source,c.chat_type FROM sessions s ORDER BY started_at DESC LIMIT 40')
# note: source column; print
rows = cur.fetchall()
for r in rows:
    dt = datetime.datetime.utcfromtimestamp(r[2]).strftime('%m-%d %H:%M') if r[2] else '?'
    print(dt,'|',r[0][:20],'|',(r[1] or '')[:45],'| msgs:',r[3],'|',r[4])

print()
print('=== Messages mentioning to-do/topic8 markers since 2026-08-24 (user role) ===')
since = int(datetime.datetime(2026,8,24,0,0).timestamp())
cur.execute("""SELECT m.session_id, m.timestamp, m.content
FROM messages m WHERE m.role='user' AND m.timestamp>?
AND (m.content LIKE '%to-do%' OR m.content LIKE '%todo%' OR m.content LIKE '%to do%'
     OR m.content LIKE '%41tCh%' OR m.content LIKE '%Topic 8%' OR m.content LIKE '%brain dump%'
     OR m.content LIKE '%#to-do-list%')
ORDER BY m.timestamp ASC""", (since,))
for s,ts,c in cur.fetchall():
    dt = datetime.datetime.utcfromtimestamp(ts).strftime('%m-%d %H:%M') if ts else '?'
    c1 = c[:300].replace('\n',' | ')
    print(dt,'|',s[:20],'|',c1)