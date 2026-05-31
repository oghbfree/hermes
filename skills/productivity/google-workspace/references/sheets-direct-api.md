# Google Sheets Direct API Pattern (Windows workaround)

## When to use this

On Windows (bash/MSYS), the `google_api.py sheets update` and `sheets append` CLI
commands fail when `--values` JSON contains single quotes, double quotes, unicode
characters, or special characters embedded in cell values. The shell mangles the
quoting and you get `unrecognized arguments` or `is not recognized` errors.

**Fix:** Call the Google Sheets REST API directly from Python's `execute_code`
using `urllib`, reading the OAuth token from disk. This completely bypasses shell
quoting.

## Token location and refresh

The token is at `~/.hermes/google_token.json`. It has these fields:
`token`, `refresh_token`, `token_uri`, `client_id`, `client_secret`, `scopes`,
`expiry`, `type`.

If the token is expired (check `expiry` field), refresh it first (see below).
The `token` field is your `access_token`.

## Pattern: Write data to a sheet

```python
import json, os, urllib.request, urllib.parse

# --- 1. Load & refresh token ---
token_file = os.path.expanduser("~/.hermes/google_token.json")
with open(token_file) as f:
    creds = json.load(f)

# Refresh if needed
refresh_data = urllib.parse.urlencode({
    "client_id": creds["client_id"],
    "client_secret": creds["client_secret"],
    "refresh_token": creds["refresh_token"],
    "grant_type": "refresh_token"
}).encode()
req = urllib.request.Request(creds["token_uri"], data=refresh_data)
with urllib.request.urlopen(req) as resp:
    creds.update(json.loads(resp.read()))
with open(token_file, 'w') as f:
    json.dump(creds, f)

token = creds["access_token"]

# --- 2. Build your data ---
sheet_id = "YOUR_SHEET_ID"
# rows is a list of lists: first element = header row
rows = [
    ["Col1", "Col2", "Col3"],
    ["val1", "val2", "val3"],
    # ... more rows
]
total_rows = len(rows)

# --- 3. Write via batchUpdate API ---
base_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values:batchUpdate"
body = {
    "valueInputOption": "RAW",
    "data": [{
        "range": f"'Sheet Name'!A1:C{total_rows}",
        "majorDimension": "ROWS",
        "values": rows
    }]
}
data = json.dumps(body).encode()
req = urllib.request.Request(base_url, data=data, headers={
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}, method="POST")
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
print(result)
```

## Pattern: Format a sheet (bold header, freeze row, column widths)

```python
# --- 4. Get sheet tab ID ---
url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
with urllib.request.urlopen(req) as resp:
    info = json.loads(resp.read())

sheet_id_num = None
for s in info["sheets"]:
    if s["properties"]["title"] == "Your Sheet Name":
        sheet_id_num = s["properties"]["sheetId"]
        break

# --- 5. Batch format ---
requests_body = {
    "requests": [
        # Bold + dark background header
        {"repeatCell": {"range": {"sheetId": sheet_id_num, "startRowIndex": 0, "endRowIndex": 1},
         "cell": {"userEnteredFormat": {"textFormat": {"bold": True},
          "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
          "horizontalAlignment": "CENTER"}},
         "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)"}},
        # Freeze first row
        {"updateSheetProperties": {"properties": {"sheetId": sheet_id_num,
         "gridProperties": {"frozenRowCount": 1}},
         "fields": "gridProperties.frozenRowCount"}},
        # Auto-resize all columns
        {"autoResizeDimensions": {"dimensions": {"sheetId": sheet_id_num,
         "dimension": "COLUMNS", "startIndex": 0, "endIndex": 8}}}
    ]
}
data = json.dumps(requests_body).encode()
url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate"
req = urllib.request.Request(url, data=data, headers={
    "Authorization": f"Bearer {token}", "Content-Type": "application/json"
}, method="POST")
with urllib.request.urlopen(req) as resp:
    print(json.loads(resp.read()))
```

## Key notes

- **Sheet names with spaces** must be single-quoted in the range string: `'Packing List'!A1:H46`
- **Range must match data exactly** — if you have 47 rows, the range must end at row 47, not 46
- **Do NOT use `urllib.parse.quote`** on the range — single quotes in sheet names go literally in the JSON body
- **`valueInputOption: "RAW"`** treats values as-is (no auto-conversion)
- This pattern works for Sheets, and the same approach works for Drive/Docs API calls from `execute_code`
