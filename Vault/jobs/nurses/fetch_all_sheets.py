import json, urllib.request, urllib.parse, os, datetime

# Use existing token
with open(r'C:\Users\User\.hermes\google_token.json', encoding='utf-8-sig') as f:
    token_data = json.load(f)
access_token = token_data['access_token']
print(f"Using existing token, expires: {token_data.get('expiry','?')}")

def fetch_sheet(sheet_id, tab_range):
    encoded_range = urllib.parse.quote(tab_range, safe='')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {access_token}'})
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read().decode('utf-8'))
    return data.get('values', [])

# All 4 sheets - nurses already has 35 rows from previous fetch, but re-fetch for completeness
sheets = {
    'nurses': {
        'id': '1JKAQMF1eUotpqp61Dd_0bbkteRe3oOB-oLwLMMdyOq4',
        'range': 'Form responses 1!A1:Z500'
    },
    'financial_literacy': {
        'id': '1GUdkRPkD5b68WorxepfMUmHjbggGu6NggWPO87tFFA8',
        'range': 'Form responses 1!A1:Z500'
    },
    'construction': {
        'id': '1Od-tUpf02eGfirjFvtUHgojsYRq2JA20IJAMOETCE4k',
        'range': 'Form responses 1!A1:Z500'
    },
    'facilitators': {
        'id': '1jxpEQRYh08pUlCQHbKygVL8vtP5CWqHupRWYx5xtQCU',
        'range': 'Form responses 1!A1:Z500'
    }
}

results = {}
for name, info in sheets.items():
    try:
        rows = fetch_sheet(info['id'], info['range'])
        results[name] = rows
        print(f"{name}: {len(rows)} rows total ({len(rows)-1} data rows)")
    except Exception as e:
        print(f"{name}: ERROR - {e}")
        results[name] = []

# Save raw data
today = datetime.date.today().strftime('%Y-%m-%d')
out_path = fr'C:\Users\User\.hermes\workspace\Vault\jobs\sheets-raw-{today}.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nSaved to {out_path}")

# Print header rows for each sheet
for name, rows in results.items():
    if rows:
        print(f"\n=== {name.upper()} HEADER ===")
        for i, col in enumerate(rows[0]):
            print(f"  col[{i}] = '{col}'")
        print(f"\n=== {name.upper()} LAST 3 DATA ROWS ===")
        for row in rows[-3:]:
            print(f"  {row[:8]}...")
