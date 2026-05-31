import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

creds_path = os.path.join(os.path.expanduser('~'), '.openclaw', 'google-sheets-creds.json')
with open(creds_path, encoding='utf-8-sig') as f:
    creds_data = json.load(f)

print("Checking credentials...")
print("Has refresh_token:", bool(creds_data.get('refresh_token')))
print("Has client_id:", bool(creds_data.get('client_id')))
print("Has client_secret:", bool(creds_data.get('client_secret')))

credentials = Credentials(
    token=None,
    refresh_token=creds_data['refresh_token'],
    client_id=creds_data['client_id'],
    client_secret=creds_data['client_secret'],
    token_uri='https://oauth2.googleapis.com/token',
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

print("Credentials valid:", credentials.valid)
print("Credentials expired:", credentials.expired if hasattr(credentials, 'expired') else 'unknown')

try:
    credentials.refresh(Request())
    print("Refresh SUCCESS!")
    print("New token:", credentials.token[:20] + '...' if credentials.token else 'None')
    
    # Save the new token
    with open(creds_path, 'w') as f:
        json.dump(creds_data, f)
    print("Credentials saved.")
except Exception as e:
    print(f"Refresh FAILED: {e}")
