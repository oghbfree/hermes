import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import GoogleAuthError

creds_path = os.path.join(os.path.expanduser('~'), '.openclaw', 'google-sheets-creds.json')
with open(creds_path, encoding='utf-8-sig') as f:
    creds_data = json.load(f)

# Try different scope formats
scopes_to_try = [
    ['https://www.googleapis.com/auth/spreadsheets.readonly'],
    ['https://www.googleapis.com/auth/spreadsheets'],
    ['https://www.googleapis.com/auth/drive.readonly'],
    ['spreadsheets.readonly'],
    ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/spreadsheets.readonly'],
]

for scopes in scopes_to_try:
    try:
        credentials = Credentials(
            token=None,
            refresh_token=creds_data['refresh_token'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret'],
            token_uri='https://oauth2.googleapis.com/token',
            scopes=scopes
        )
        credentials.refresh(Request())
        print(f"SUCCESS with scopes: {scopes}")
        print(f"Token: {credentials.token[:20]}...")
        break
    except Exception as e:
        print(f"Failed with scopes {scopes}: {e}")
