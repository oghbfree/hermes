import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds_path = os.path.join(os.path.expanduser('~'), '.openclaw', 'google-sheets-creds.json')
with open(creds_path, encoding='utf-8-sig') as f:
    creds_data = json.load(f)

credentials = Credentials(
    token=None,
    refresh_token=creds_data['refresh_token'],
    client_id=creds_data['client_id'],
    client_secret=creds_data['client_secret'],
    token_uri='https://oauth2.googleapis.com/token',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

if not credentials.valid:
    credentials.refresh(Request())

service = build('sheets', 'v4', credentials=credentials)

# Sheet IDs from previous sessions
sheets = {
    'Nurses': '1JKAQMF1eUotpqp61Dd_0bbkteRe3oOB-oLwLMMdyOq4',
    'Construction': '1Od-tUpfLRiWvOoOmd7DlG5FQVYEo7J3Qi7frIDIP3YK',
    'Facilitators_Robotics': '1jxpEQRqUC3yt2fcRNX7Ay5GTTE6PGETbf0r0RYgFoWw',
    'Financial_Literacy': '1GUdkRPkD5b68WorxepfMUmHjbggGu6NggWPO87tFFA8',
}

results = {}
for name, sid in sheets.items():
    try:
        result = service.spreadsheets().values().get(spreadsheetId=sid, range='Sheet1!A:Z').execute()
        rows = result.get('values', [])
        results[name] = rows
        print(f'{name}: {len(rows)} rows')
    except Exception as e:
        results[name] = {'error': str(e)}
        print(f'{name}: ERROR - {e}')

out_path = os.path.join(os.path.expanduser('~'), '.hermes', 'workspace', 'memories', 'jobs', 'sheets-raw-2026-05-28.json')
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f'\nSaved to {out_path}')
