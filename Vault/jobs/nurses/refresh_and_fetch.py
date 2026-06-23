import json, urllib.request, urllib.parse, datetime

with open(r'C:\Users\User\.hermes\google_token.json', encoding='utf-8-sig') as f:
    creds = json.load(f)

params = urllib.parse.urlencode({
    'client_id': creds['client_id'],
    'client_secret': creds['client_secret'],
    'refresh_token': creds['refresh_token'],
    'grant_type': 'refresh_token'
}).encode('utf-8')

req = urllib.request.Request('https://oauth2.googleapis.com/token', data=params)
resp = urllib.request.urlopen(req, timeout=15)
result = json.loads(resp.read().decode('utf-8'))

with open(r'C:\Users\User\.hermes\workspace\memories\jobs\tmp_access_token.txt', 'w') as f:
    f.write(result['access_token'])

creds['access_token'] = result['access_token']
creds['token'] = result['access_token']
creds['expires_in'] = result['expires_in']
creds['expiry'] = (datetime.datetime.utcnow() + datetime.timedelta(seconds=result['expires_in'])).isoformat() + 'Z'
with open(r'C:\Users\User\.hermes\google_token.json', 'w') as f:
    json.dump(creds, f, indent=2)
print('Token refreshed, length:', len(result['access_token']))

with open(r'C:\Users\User\.hermes\workspace\memories\jobs\tmp_access_token.txt') as f:
    ACCESS_TOKEN = f.read().strip()

def fetch_sheet(sheet_id):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/A1:Z500'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode('utf-8')).get('values', [])

SHEETS = {
    'nurses': '1JKAQMF1eUotpqp61Dd_0bbkteRe3oOB-oLwLMMdyOq4',
    'financial-literacy': '1GUdkRPkD5b68WorxepfMUmHjbggGu6NggWPO87tFFA8',
    'construction': '1Od-tUpf02eGfirjFvtUHgojsYRq2JA20IJAMOETCE4k',
    'facilitators': '1jxpEQRYh08pUlCQHbKygVL8vtP5CWqHupRWYx5xtQCU'
}

date_str = datetime.date.today().strftime('%Y-%m-%d')
out = {}
for name, sid in SHEETS.items():
    try:
        data = fetch_sheet(sid)
        out[name] = data
        print(f'OK {name}: {len(data)} rows')
    except Exception as e:
        print(f'ERROR {name}: {e}')
        out[name] = []

out_path = r'C:\Users\User\.hermes\workspace\memories\jobs\sheets-raw-' + date_str + '.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print('Saved to', out_path)
