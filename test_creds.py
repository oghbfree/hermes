import json, os
creds_path = os.path.join(os.path.expanduser('~'), '.openclaw', 'google-sheets-creds.json')
with open(creds_path, encoding='utf-8-sig') as f:
    creds = json.load(f)
print('Credentials loaded')
print('client_id:', creds['client_id'][:10])
