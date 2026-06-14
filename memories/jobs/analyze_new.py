import json, datetime

today = datetime.date.today().strftime('%Y-%m-%d')

with open(fr'C:\Users\User\.hermes\workspace\memories\jobs\sheets-raw-{today}.json', encoding='utf-8') as f:
    results = json.load(f)

# State files (lastProcessedRow = data rows already seen)
# Nurses: lastProcessedRow 34, Financial: 1, Construction: 7, Facilitators: 3
# Sheet rows include header, so data rows = total_rows - 1

state = {
    'nurses': {'lastProcessedRow': 34, 'lastTotal': 34},
    'financial_literacy': {'lastProcessedRow': 1, 'lastTotal': 1},
    'construction': {'lastProcessedRow': 7, 'lastTotal': 7},
    'facilitators': {'lastProcessedRow': 3, 'lastTotal': 3}
}

print("=== NEW APPLICATIONS ANALYSIS ===\n")

for name, rows in results.items():
    total_with_header = len(rows)
    total_data_rows = total_with_header - 1  # subtract header
    prev_processed = state[name]['lastProcessedRow']
    new_rows_count = total_data_rows - prev_processed

    print(f"--- {name.upper()} ---")
    print(f"  Total in sheet: {total_with_header} (header + {total_data_rows} data)")
    print(f"  Previously processed: {prev_processed}")
    print(f"  NEW: {new_rows_count}")
    print()

    if new_rows_count > 0:
        header = rows[0]
        new_data_rows = rows[prev_processed + 1: prev_processed + 1 + new_rows_count]
        for i, row in enumerate(new_data_rows):
            print(f"  === NEW APPLICANT #{i+1} ===")
            for j, val in enumerate(row):
                col_name = header[j] if j < len(header) else f"col[{j}]"
                if val.strip():  # Only print non-empty fields
                    print(f"    {col_name}: {val}")
            print()
    print()
