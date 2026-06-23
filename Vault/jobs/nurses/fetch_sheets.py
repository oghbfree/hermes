import json, urllib.request, urllib.parse, os, datetime

# Load creds
with open(r'C:\Users\User\.openclaw\google-sheets-creds.json', encoding='utf-8-sig') as f:
    creds = json.load(f)

# Refresh token
params = urllib.parse.urlencode({
    'client_id': creds['client_id'],
    'client_secret': creds['client_secret'],
    'refresh_token': creds['refresh_token'],
    'grant_type': 'refresh_token'
}).encode('utf-8')
req = urllib.request.Request("https://oauth2.googleapis.com/token", data=params)
resp = urllib.request.urlopen(req, timeout=15)
token_resp = json.loads(resp.read().decode('utf-8'))
access_token = token_resp['access_token']
print(f"Token refreshed OK, expires_in={token_resp.get('expires_in')}")
print(f"Scopes: {token_resp.get('scope', 'N/A')}")

# Save refreshed token back
token_path = r'C:\Users\User\.hermes\google_token.json'
try:
    with open(token_path, encoding='utf-8-sig') as f:
        existing = json.load(f)
except:
    existing = {}
existing['access_token'] = access_token
existing['token'] = access_token
existing['expiry'] = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=token_resp.get('expires_in', 3599))).isoformat().replace('+00:00','Z')
with open(token_path, 'w') as f:
    json.dump(existing, f, indent=2)
print("Token saved to google_token.json")

def fetch_sheet(sheet_id, tab_range):
    encoded_range = urllib.parse.quote(tab_range, safe='')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}"
    print(f"  Fetching: {url[:100]}...")
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {access_token}'})
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read().decode('utf-8'))
    return data.get('values', [])

# Fetch all 4 sheets
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
        print(f"{name}: {len(rows)} rows (including header)")
    except Exception as e:
        print(f"{name}: ERROR - {e}")
        # Try to read more error details
        try:
            if hasattr(e, 'read'):
                print(f"  Error body: {e.read().decode('utf-8', errors='replace')}")
        except:
            pass
        results[name] = []

# Save raw data
today = datetime.date.today().strftime('%Y-%m-%d')
out_path = fr'C:\Users\User\.hermes\workspace\memories\jobs\sheets-raw-{today}.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nSaved to {out_path}")

# Print summary
for name, rows in results.items():
    print(f"\n=== {name.upper()} ===")
    if rows:
        print(f"  Header: {rows[0][:10]}...")
        print(f"  Total rows: {len(rows)} (data rows: {len(rows)-1})")
        if len(rows) > 1:
            print(f"  Last row: {rows[-1][:8]}...")
