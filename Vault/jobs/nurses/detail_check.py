import json

with open(r'C:\Users\User\.hermes\workspace\memories\jobs\sheets-raw-2026-05-29.json', encoding='utf-8') as f:
    data = json.load(f)

# New Construction applicant - row 7 (index 7)
construction_rows = data['Construction']
print("=== NEW CONSTRUCTION APPLICANT (Row 7) ===")
new_row = construction_rows[7]
headers = construction_rows[0]
for i, (h, v) in enumerate(zip(headers, new_row)):
    print(f"  [{i}] {h}: {v}")

print("\n=== Facilitators (all rows) ===")
fac_rows = data['Facilitators_Robotics']
for i, row in enumerate(fac_rows):
    if i == 0:
        continue
    ts = row[0] if len(row) > 0 else ''
    nm = row[2].strip() if len(row) > 2 and row[2] else '(empty)'
    ph = row[3].strip() if len(row) > 3 and row[3] else ''
    loc = row[5].strip() if len(row) > 5 and row[5] else ''
    qual = row[6].strip() if len(row) > 6 and row[6] else ''
    print(f"  Row {i}: [{ts}] {nm} | ph:{ph} | loc:{loc} | qual:{qual}")

print("\n=== Nurses (check last few, already at 34) ===")
nurse_rows = data['Nurses']
print(f"  Total rows: {len(nurse_rows)} (data: {len(nurse_rows)-1})")
for i, row in enumerate(nurse_rows[-3:]):
    idx = len(nurse_rows) - 3 + i
    ts = row[0] if len(row) > 0 else ''
    nm = row[2].strip() if len(row) > 2 and row[2] else '(empty)'
    print(f"  Row {idx}: [{ts}] {nm}")
