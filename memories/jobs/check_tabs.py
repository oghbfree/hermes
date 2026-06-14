import json, urllib.request, urllib.parse, os, datetime

# Use existing token
with open(r'C:\Users\User\.hermes\google_token.json', encoding='utf-8-sig') as f:
    token_data = json.load(f)
access_token = token_data['access_token']

def get_sheet_metadata(sheet_id):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?fields=sheets.properties.title"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {access_token}'})
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read().decode('utf-8'))
    return [s['properties']['title'] for s in data.get('sheets', [])]

sheet_ids = {
    'financial_literacy': '1GUdkRPkD5b68WorxepfMUmHjbggGu6NggWPO87tFFA8',
    'construction': '1Od-tUpf02eGfirjFvtUHgojsYRq2JA20IJAMOETCE4k',
    'facilitators': '1jxpEQRYh08pUlCQHbKygVL8vtP5CWqHupRWYx5xtQCU'
}

for name, sid in sheet_ids.items():
    try:
        tabs = get_sheet_metadata(sid)
        print(f"{name}: {tabs}")
    except Exception as e:
        print(f"{name}: ERROR - {e}")
