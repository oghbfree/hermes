import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds_path = os.path.join(os.path.expanduser('~'), '.openclaw', 'google-sheets-creds.json')
with open(creds_path) as f:
    creds_data = json.load(f)

credentials = Credentials(
    token=None,
    refresh_token=creds_data['refresh_token'],
    client_id=creds_data['client_id'],
    client_secret=creds_data['client_secret'],
    token_uri='https://oauth2.googleapis.com/token',
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

if not credentials.valid:
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        print('Credentials invalid')
        exit(1)

service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1GUdkRPkD5b68WorxepfMUmHjbggGu6NggWPO87tFFA8'
range_name = 'Sheet1!A:Z'
result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
rows = result.get('values', [])
print(f'Total rows: {len(rows)}')
if rows:
    print('First row:', rows[0])
    print('Second row:', rows[1] if len(rows) > 1 else None)
