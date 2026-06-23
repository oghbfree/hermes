import json

with open(r'C:\Users\User\.hermes\workspace\memories\jobs\sheets-raw-2026-06-22.json', encoding='utf-8') as f:
    new_data = json.load(f)
with open(r'C:\Users\User\.hermes\workspace\memories\jobs\sheets-raw-2026-06-21.json', encoding='utf-8') as f:
    old_data = json.load(f)

roles = ['nurses', 'financial_literacy', 'construction', 'facilitators']
labels = {'nurses':'Nurses','financial_literacy':'Financial Literacy','construction':'Construction','facilitators':'Facilitators'}

print('=== ROW COUNT COMPARISON ===')
total_new = 0
for r in roles:
    nc = len(new_data.get(r,[])) - 1
    oc = len(old_data.get(r,[])) - 1
    d = nc - oc
    sign = '+' if d > 0 else ''
    print('  %s: %d -> %d (%s%d)' % (labels[r], oc, nc, sign, d))
    total_new += d
print('  TOTAL NEW: %d' % total_new)

print()
print('=== LAST ROW TIMESTAMPS ===')
for r in roles:
    rows = new_data.get(r,[])
    if len(rows) > 1:
        lr = rows[-1]
        name = lr[2] if len(lr) > 2 else 'N/A'
        print('  %s: %s | %s' % (labels[r], lr[0], name))

print()
print('=== NEW ROWS DETAIL ===')
for r in roles:
    new_rows = new_data.get(r,[])
    old_rows = old_data.get(r,[])
    if not new_rows or not old_rows:
        continue
    old_timestamps = set(row[0] for row in old_rows[1:])
    new_entries = [row for row in new_rows[1:] if row[0] not in old_timestamps]
    if new_entries:
        print('  [%s] %d new row(s):' % (labels[r], len(new_entries)))
        for entry in new_entries:
            nm = entry[2] if len(entry) > 2 else '?'
            loc = entry[6] if len(entry) > 6 else '?'
            print('    - %s | %s | %s' % (entry[0], nm, loc))
    else:
        print('  [%s] No new rows' % labels[r])
