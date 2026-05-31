import json, sys

data = json.load(sys.stdin)
print(f"Total rows (including header): {len(data)}")
print(f"Data rows (excluding header): {len(data) - 1}")

# Print all rows with index
for i, row in enumerate(data):
    if i == 0:
        print(f"  Row {i}: HEADER - {row[:3]}...")
    else:
        name = row[2].strip() if len(row) > 2 else "N/A"
        phone = row[5].strip() if len(row) > 5 else "N/A"
        location = row[6].strip() if len(row) > 6 else "N/A"
        qual = row[7].strip() if len(row) > 7 else "N/A"
        nmc = row[8].strip() if len(row) > 8 else "N/A"
        exp = row[10].strip() if len(row) > 10 else "N/A"
        driver = row[15].strip() if len(row) > 15 else "N/A"
        car = row[16].strip() if len(row) > 16 else "N/A"
        timestamp = row[0] if len(row) > 0 else "N/A"
        print(f"  Row {i}: {name} | {phone} | {location} | {qual} | NMC:{nmc} | Exp:{exp} | Driver:{driver} | Car:{car} | {timestamp}")
