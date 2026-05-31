# Recruitment Tracking Pipeline

> Formerly the `recruitment-tracking` skill. Consolidated into `business-operations-tracking`.

Monitor job application pipelines stored in Google Sheets. Detect new submissions since last check, filter and rank candidates, update tracking state files, and produce structured reports.

## Pipelines

| Role | Sheet ID | Tab | Status |
|------|----------|-----|--------|
| Nurses | `1JKAQMF1eUotpqp61Dd_0bbkteRe3oOB-oLwLMMdyOq4` | `Form responses 1` | ✅ Active |
| Financial Literacy | `1GUdkRPkD5b68WorxepfMUmHjbggGu6NggWPO87tFFA8` | `Form responses 1` | ✅ Active |
| Construction | `1Od-tUpf02eGfirjFvtUHgojsYRq2JA20IJAMOETCE4k` | `Form responses 1` | ✅ Active |
| Facilitators/Robotics | `1jxpEQRYh08pUlCQHbKygVL8vtP5CWqHupRWYx5xtQCU` | `Form responses 1` | ✅ Active |

## State Files

Each pipeline has a JSON state file for differential checking:

| Pipeline | State File |
|----------|-----------|
| Nurses | `~/.hermes/workspace/memories/jobs/last-check-nurses.json` |
| Financial Literacy | `~/.hermes/workspace/memories/jobs/last-check-financial-literacy.json` |
| Construction | `~/.hermes/workspace/memories/jobs/last-check-construction.json` |
| Facilitators | `~/.hermes/workspace/memories/jobs/last-check-facilitators.json` |

State file schema:
```json
{
  "lastCheckDate": "YYYY-MM-DD",
  "lastProcessedRow": 32,
  "totalRows": 32,
  "error": null
}
```

## Workflow

## Auth Method

### Google OAuth2 Direct API (current, ~2026-05-25+)
The `gws` CLI and `gcloud` are NOT installed on the Windows host. Use direct Python OAuth2 instead.

Token file: `~/.hermes/google_token.json`
Credential files: `~/.hermes/google_client_secret.json` (has `client_id`, `client_secret`, `refresh_token`)

Workflow:
1. Load `google_token.json`, check `expiry` field
2. If expired (likely — tokens last 1hr), POST to `https://oauth2.googleapis.com/token` with `refresh_token`, `client_id`, `client_secret`, `grant_type=refresh_token`
3. Save the new `access_token` and updated `expiry` back to `google_token.json`
4. Use the `access_token` in `Authorization: Bearer <token>` header for all Sheets API calls

Pattern (works in execute_code):
```python
import json, urllib.request, urllib.parse, datetime

with open(r'C:\Users\User\.hermes\google_token.json') as f:
    token_data = json.load(f)
# POST refresh_token to https://oauth2.googleapis.com/token
# Update token_data['access_token'] and token_data['expiry']
# Use access_token in headers for Sheets API
```

Sheet API call pattern:
```python
url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/A1:Z"
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {access_token}'})
resp = urllib.request.urlopen(req)
rows = json.loads(resp.read().decode('utf-8')).get('values', [])
```

### Legacy method (DO NOT USE — CLI not installed)
```bash
# This does NOT work on the Windows host — gws not in PATH
GAPI="python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py"
$GAPI sheets get SHEET_ID "TabName!A1:Z200"
```

### 3. Detect New Applications
Compare `totalRows` from the sheet against `lastProcessedRow` in the state file. New rows = `totalRows - lastProcessedRow`.

**Note:** Sheet API returns ALL columns. For Nurses, columns beyond col 18 (Q/R/S) contain the long-form interview questions. Financial and Facilitator sheets have different column layouts — read the header row to map them.

### 4. Filter & Rank Candidates

## Column Mappings

### Nurses (sheet has evolved — cols 0-25+ as of 2026-05)
Key columns (0-indexed):
- 0: Timestamp
- 2: Full Name
- 3: Male/Female
- 4: *(new)* Interview Times
- 5: Phone Number
- 6: Location
- 7: Qualification
- 8: NMC Registered
- 9: NMC PIN
- 10: Years of experience
- 11: Evidence of experience
- 12: Willing with CCTV
- 13: Live-in/commute/both
- 14: Languages
- 15: Driver's Licence
- 16: Has car
- 17: WhatsApp vitals
- 18: CV upload (Google Drive link)
- 19-25+: Long-form interview questions

**Nursing priority criteria (in order):**
1. NMC Registered (col 8: "Yes")
2. 3-5+ years experience (col 10)
3. Has driver's licence (col 15: "Yes")
4. Has car (col 16: "Yes")
5. Completed interview questions (cols 19-25 non-empty)
6. Location proximity to Accra/Greater Accra / Weija

### Financial Literacy
Key columns: Timestamp(0), Email(1), Full Name(2), Gender(3), Phone(4), Email(5), Location(6), Education(7), Teaching exp with kids 7-12(8), Describe experience(9), Digital tools comfort 1-10(10), Financial topics(11), Runs business?(12), Compound interest for 7yo(13), Availability(14), Video intro(15), CV(16), Expected hourly rate GHS(17), Questions(18), Coding/Robotics exp(19)

### Construction
Key columns: Timestamp(0), Email(1), Full Name(2), Gender(3), WhatsApp w/ country code(4), Location(5), Email(6), Primary Trade(7), Years exp(8), Foreman exp?(9), Machines operate(10), + machine-specific experience columns(11-24), Owns tools?(25), Safety certs(26)

### Facilitators/Robotics (Akoma) — cols 0-25
Key columns: Timestamp(0), Email(1), Full Name(2), Phone(3), Email(4), Location(5), Qualification(6), Field of Study(7), Employment Status(8), Taught kids 7-14?(9), Describe exp(10), mBlock comfort 1-5(11), mBot experience?(12), Debugging scenario(13), Autism/inclusive ed exp(14), Sensory overload response(15), John Protocol OK?(16), Zobase clock-in OK?(17), Commission-based OK?(18), **Financial liability for equipment(19), Own laptop?(20), Availability/days(21), LinkedIn profile(22), How heard(23), CV link(24), Data consent(25)**

**Facilitator priority criteria (in order):**
1. mBot experience (col 12: "Yes")
2. mBlock comfort 4-5/5 (col 11)
3. Has own laptop (col 20: "Yes")
4. Full week or weekend availability (col 21)
5. Strong autism/sensory response answer (col 14-15)
6. IT/CS degree field (col 7)
7. Teaching experience with children (col 9-10)

### 5. Update State Files
After processing, update the state file with new `lastProcessedRow`, `totalRows`, and `lastCheckDate`.

### 6. Generate Report
Save full report to `~/.hermes/workspace/memories/jobs/APPLICATIONS-REPORT-YYYY-MM-DD.md`.

Use the report template at `references/report-template-recruitment.md`.

### 7. Post Summary to Telegram
Deliver a concise summary to the jobs topic. Lead with new applicant count, highlight top picks, note blockers.

## Cron Delivery

The `job-applications-check` cron job (ID: `c4ae96f821b1`, schedule: `0 8 * * *`) delivers to `origin` which routes to Telegram chat `-1003784520976`, thread `20` (memory-review).

**Note:** The jobs/recruitment channel is topic `28`. If reports should go to the jobs topic instead of memory-review, update the cron's deliver field to `telegram:-1003784520976:28`.

## Auth — Working Pattern (2026-05-29 Update)

The `execute_code` tool's sandbox **blocks outbound HTTPS to Google APIs** (OAuth + Sheets). Do NOT use `execute_code` + `urllib` for token refresh or sheet fetching.

**Working approach — Terminal + curl + script file:**

1. Refresh token via curl in terminal:
```bash
curl -s --connect-timeout 10 "https://oauth2.googleapis.com/token" \
  -X POST -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=...&client_secret=...&refresh_token=...&grant_type=refresh_token"
```

2. Write a Python script to a temp path and execute with full Python path:
```bash
/c/Users/User/AppData/Local/Programs/Python/Python314/python.exe /path/to/script.py
```

**Why:** `execute_code` runs in a sandboxed temp directory and **cannot reach `oauth2.googleapis.com` or `sheets.googleapis.com`** — connections time out after ~100s. The `terminal` tool's curl can reach Google APIs. Once you have the access token via curl, write it into a script file and run that script via terminal with the full Python path.

**Credential file priority:** Use `~/.hermes/google_token.json` as the **primary** credential file — it has `refresh_token`, `client_id`, `client_secret`, and full scopes (`spreadsheets`, `drive`, `gmail.*`, `calendar`, `documents`). The `~/.openclaw/google-sheets-creds.json` is a **known-dead backup** as of 2026-05-31 — its `refresh_token` returns `invalid_grant` and should not be used. If `google_token.json` refresh ever fails, the credential must be re-authorized from scratch rather than falling back to `.openclaw`.

**Token extraction — do NOT pipe through shell variables.** The access token is ~254 chars and gets truncated when passed through `$(sed ...)` or shell variable interpolation in `curl -d "${TOKEN}"`. Instead, have Python write the token directly to a temp file, then read that file in the fetch script:

```python
# Step 1: Refresh token and save FULL access token to temp file (run via terminal)
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
# Save token to temp file for the fetch script
with open(r'C:\Users\User\.hermes\workspace\memories\jobs\tmp_access_token.txt', 'w') as f:
    f.write(result['access_token'])
# Also update google_token.json
creds['access_token'] = result['access_token']
creds['token'] = result['access_token']
creds['expires_in'] = result['expires_in']
creds['expiry'] = (datetime.datetime.utcnow() + datetime.timedelta(seconds=result['expires_in'])).isoformat() + 'Z'
with open(r'C:\Users\User\.hermes\google_token.json', 'w') as f:
    json.dump(creds, f, indent=2)
print('Token refreshed, length:', len(result['access_token']))
```

Then in the fetch script, read the token from the temp file:
```python
with open(r'C:\Users\User\.hermes\workspace\memories\jobs\tmp_access_token.txt') as f:
    ACCESS_TOKEN = f.read().strip()
```

**Why:** `execute_code` runs in a sandboxed temp directory and **cannot reach `oauth2.googleapis.com` or `sheets.googleapis.com`** — connections time out after ~100s. The `terminal` tool's Python can reach Google APIs. Always do the token refresh in a Python script run via `terminal`, never via `execute_code`.

### Sheet Fetch Script Pattern

Write a script like `fetch_sheets.py` to `~/.hermes/workspace/memories/jobs/`:

```python
import json, urllib.request, datetime

# Read access token from temp file (written by refresh step above)
with open(r'C:\Users\User\.hermes\workspace\memories\jobs\tmp_access_token.txt') as f:
    ACCESS_TOKEN = f.read().strip()

def fetch_sheet(sheet_id):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/A1:Z"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read().decode('utf-8')).get('values', [])

SHEETS = {
    "nurses": "1JKAQMF1eUotpqp61Dd_0bbkteRe3oOB-oLwLMMdyOq4",
    "financial-literacy": "1GUdkRPkD5b68WorxepfMUmHjbggGu6NggWPO87tFFA8",
    "construction": "1Od-tUpf02eGfirjFvtUHgojsYRq2JA20IJAMOETCE4k",
    "facilitators": "1jxpEQRYh08pUlCQHbKygVL8vtP5CWqHupRWYx5xtQCU"
}

date_str = datetime.date.today().strftime("%Y-%m-%d")
out = {}
for name, sid in SHEETS.items():
    data = fetch_sheet(sid)
    out[name] = data
    print(f"OK {name}: {len(data)} rows (including header)")

out_path = rf"C:\Users\User\.hermes\workspace\memories\jobs\sheets-raw-{date_str}.json"
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"Saved to {out_path}")
```

Run both scripts via terminal with the full Python path:
```bash
/c/Users/User/AppData/Local/Programs/Python/Python314/python.exe /path/to/refresh_and_fetch.py
```

**Windows Python path:** `python3` alias redirects to Microsoft Store. Always use full path `C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe`.

## Auth — Credential Status (2026-05-31)

| File | Location | Status | Notes |
|------|----------|--------|-------|
| `google_token.json` | `~/.hermes/` | ✅ **PRIMARY** — working | Has `refresh_token`, `client_id`, `client_secret`, full scopes. Refresh via Python in terminal (not `execute_code`). |
| `google-sheets-creds.json` | `~/.openclaw/` | ❌ **DEAD** as of 2026-05-31 | `refresh_token` returns `invalid_grant`. Do not use. |

**Save-back**: Always write the refreshed token back to `google_token.json` (overwrite `access_token`, `token`, `expiry`, `expires_in` fields). The `.openclaw` file is not updated and should be ignored.

## Known Blockers

- **WhatsApp outage**: Cannot contact candidates even when identified
- ~~**3/4 sheets permission denied**~~ ✅ **RESOLVED ~2026-05-27** — All 4 sheets accessible
- **Empty name fields**: Some rows have name empty but phone/location filled (e.g., row 30 in nurses sheet). Check phone column as fallback identifier.
- **Cron delivery routing**: The cron job's `origin` routes to `thread_id: 20` (memory-review). Reports on new sessions by default go to whatever the cron's `deliver` field is set to — verify and update to topic 28 if needed.
- **Sheet snapshot accumulation**: `sheets-raw-*.json` files pile up in `memories/jobs/`. Only the latest is needed for diffing; older ones can be cleaned up.

## Current Pipeline Stats (2026-05-31)

| Role | Total | Since Last | NMC/Key Qual | Drivers |
|------|-------|------------|--------------|---------|
| Nurses | 34 | 0 | 22 NMC (65%) | 3 licence, 1 car |
| Financial Literacy | 1 | 0 | — | — |
| Construction | 7 | 0 | — | — |
| Facilitators/Robotics | 3 | 0 | — | — |
| **TOTAL** | **45** | **0** | | |

**New this cycle:** None. Pipeline steady since 2026-05-30.

## Previous Cycle (2026-05-30)

| Role | Total | Since Last | NMC/Key Qual | Drivers |
|------|-------|------------|--------------|---------|
| Nurses | 34 | 0 | 22 NMC (65%) | 3 licence, 1 car |
| Financial Literacy | 1 | 0 | — | — |
| Construction | 7 | +1 | — | — |
| Facilitators/Robotics | 3 | 0 | — | — |
| **TOTAL** | **45** | **+1** | | |

**New 2026-05-29:** Amane John — Janitorial (non-trade), 10+ yrs, Labadi, 0546670381. Limited construction machine skills; general labourer candidate.

## Tips

- On Windows, the `python3` alias redirects to Microsoft Store — use the full path `C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe` (confirm exact path with `which python` or `find` at session start)
- Use absolute paths: `/c/Users/User/...` or `C:\\Users\\User\\...`
- The `~` expansion doesn't work in `GAPI=` assignment on Windows — use full path
- Pipe sheet output through `scripts/parse_nurses.py` for reliable JSON processing
- Always read the state file BEFORE reading the sheet to know what's new
- If `lastProcessedRow` equals sheet row count, skip the sheet read entirely
- **Windows `execute_code` sandbox**: The `execute_code` tool's sandbox **blocks outbound HTTPS** to Google APIs. Do NOT use `execute_code` + `urllib` for token refresh or sheet fetching. Use `terminal` + Python script for token refresh, then write a script file and run it via `terminal` with the full Python path.
- **⚠️ Token truncation via shell pipe**: Do NOT extract the access token via `$(sed -n '1p' file)` or shell variable interpolation in curl — the token is ~254 chars and gets silently truncated to ~16 chars. Always have Python write the full token directly to a temp file, then read that file in the downstream fetch script.
- **Sheet IDs location**: Also documented in `skills/productivity/google-workspace/SKILL.md` lines 345-347 — cross-reference if IDs seem wrong
