import json, urllib.request, urllib.parse, datetime

with open(r'C:\Users\User\.hermes\google_token.json', encoding='utf-8-sig') as f:
    creds = json.load(f)

print("Attempting token refresh...")
print("refresh_token:", repr(creds['refresh_token'][:20]))
print("client_id:", creds['client_id'][:20])

params = urllib.parse.urlencode({
    'client_id': creds['client_id'],
    'client_secret': creds['client_secret'],
    'refresh_token': creds['refresh_token'],
    'grant_type': 'refresh_token'
}).encode('utf-8')

try:
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=params)
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read().decode('utf-8'))
    print("SUCCESS! Token refreshed.")
    print("access_token prefix:", result['access_token'][:20])
    print("expires_in:", result.get('expires_in'))
    
    # Save the new token
    creds['access_token'] = result['access_token']
    creds['token'] = result['access_token']
    creds['expires_in'] = result['expires_in']
    creds['expiry'] = (datetime.datetime.utcnow() + datetime.timedelta(seconds=result['expires_in'])).isoformat() + 'Z'
    with open(r'C:\Users\User\.hermes\google_token.json', 'w') as f:
        json.dump(creds, f, indent=2)
    print("Token saved to google_token.json")
    
    # Also save to temp file for fetch script
    with open(r'C:\Users\User\.hermes\workspace\memories\jobs\tmp_access_token.txt', 'w') as f:
        f.write(result['access_token'])
    print("Access token saved to tmp_access_token.txt")
    
except Exception as e:
    print("FAILED:", e)
