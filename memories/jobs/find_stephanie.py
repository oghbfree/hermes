import json, urllib.request

tok_file = open(r'C:\Users\User\.hermes\workspace\memories\jobs\tmp_access_token.txt')
ACCESS_TOKEN = tok_file.read().strip()
tok_file.close()

sheet_id = '1JKAQMF1eUotpqp61Dd_0bbkteRe3oOB-oLwLMMdyOq4'
url = 'https://sheets.googleapis.com/v4/spreadsheets/' + sheet_id + '/values/A1:Z'
req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + ACCESS_TOKEN})
resp = urllib.request.urlopen(req, timeout=15)
data = json.loads(resp.read().decode('utf-8')).get('values', [])

print('Total rows:', len(data))
print()

# Print header with column indices
print('=== HEADER ===')
for j, val in enumerate(data[0]):
    print('Col ' + str(j) + ': ' + val)
print()

# Find Stephanie Agyemang
for i, row in enumerate(data):
    if len(row) > 2:
        name = row[2].strip()
        if 'Stephanie' in name and 'Agyemang' in name:
            print('=== Stephanie Agyemang at row ' + str(i+1) + ' ===')
            for j in range(len(row)):
                print('Col ' + str(j) + ': ' + row[j])
            break
