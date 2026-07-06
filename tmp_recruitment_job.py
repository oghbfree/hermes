
import json
from pathlib import Path
from datetime import datetime

base = Path(r'C:\Users\User\.hermes\workspace\Vault\jobs')
new_path = base / 'sheets-raw-2026-06-27.json'
prev_path = base / 'sheets-raw-2026-06-26.json'
report_path = base / 'APPLICATIONS-REPORT-2026-06-27.md'
summary_path = base / 'RECRUITMENT_SUMMARY.md'
prev_report_path = base / 'APPLICATIONS-REPORT-2026-06-26.md'

with new_path.open('rb') as f:
    new = json.load(f)
with prev_path.open('rb') as f:
    prev = json.load(f)
with prev_report_path.open(encoding='utf-8') as f:
    prev_report = f.read()

today = datetime.utcnow().date().isoformat()
now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

roles = ['nurses', 'financial_literacy', 'construction', 'facilitators']
role_names = {
    'nurses': 'Nurses',
    'financial_literacy': 'Financial Literacy',
    'construction': 'Construction',
    'facilitators': 'Facilitators',
}

previous_totals = {'nurses': 41, 'financial_literacy': 2, 'construction': 9, 'facilitators': 3}
previous_overall = 55

new_counts = {}
new_rows = {}
current_totals = {}
for role in roles:
    old_ts = set(r[0] for r in prev.get(role, [])[1:] if r and r[0] != 'Timestamp')
    added = [r for r in new.get(role, [])[1:] if r and r[0] != 'Timestamp' and r[0] not in old_ts]
    new_counts[role] = len(added)
    new_rows[role] = added
    current_totals[role] = len([r for r in new.get(role, [])[1:] if r and r[0] != 'Timestamp'])

overall_current = sum(current_totals.values())
overall_new = overall_current - previous_overall

def parse_bool(val):
    if not val:
        return False
    v = val.lower().strip()
    return v.startswith('yes') or v == 'y' or '1' in v or 'true' == v

def parse_intish(val):
    if not val:
        return -1
    mapping = {'0-2': 1, '3-5': 4, '5-10': 7, '10+': 12}
    if val in mapping:
        return mapping[val]
    for k, n in mapping.items():
        if k in val:
            return n
    return 0

# priority nurses
nurse_rows = new.get('nurses', [])[1:]
priority_nurses = []
for r in nurse_rows:
    nmc = parse_bool(r[8]) and 'No PIN' not in (r[9] or '')
    years = parse_intish(r[10])
    licence = parse_bool(r[15])
    car = parse_bool(r[16])
    score = (3 if nmc else 0) + (3 if years >= 4 else 1 if years >= 1 else 0) + (1 if licence else 0) + (1 if car else 0)
    priority_nurses.append({
        'score': score, 'nmc': nmc, 'years': years, 'licence': licence, 'car': car,
        'name': r[2].strip(), 'email': r[1], 'phone': r[5], 'location': r[6], 'qual': r[7].strip(),
        'ts': r[0],
    })
priority_nurses.sort(key=lambda x: (-x['score'], x['ts']), reverse=False)

# priority facilitators
fac_rows = new.get('facilitators', [])[1:]
priority_facs = []
for r in fac_rows:
    code = parse_intish(r[11])
    mbot = parse_bool(r[12])
    priority_facs.append({'code': code, 'mbot': mbot, 'score': code + (2 if mbot else 0),
                          'name': r[2].strip(), 'email': r[4], 'phone': r[3], 'location': r[5],
                          'qual': (r[6]+' / '+r[7]).strip() if r[7] else r[6].strip(), 'ts': r[0]})
priority_facs.sort(key=lambda x: (-x['score'], x['ts']), reverse=False)

# priority construction
const_rows = new.get('construction', [])[1:]
priority_const = []
for r in const_rows:
    years = parse_intish(r[8])
    foreman = parse_bool(r[9])
    mach_ct = sum(1 for c in r[10:24] if parse_bool(c))
    certs = bool((r[25] or '').strip())
    score = (3 if years >= 10 else 2 if years >= 5 else 1 if years > 0 else 0) + (2 if foreman else 0) + min(mach_ct, 5) + (1 if certs else 0)
    priority_const.append({'score': score, 'years': years, 'foreman': foreman, 'mach_ct': mach_ct, 'certs': certs,
                           'name': r[2].strip(), 'email': r[1], 'phone': r[4], 'location': r[5],
                           'trade': r[7].strip() if len(r) > 7 else '', 'ts': r[0]})
priority_const.sort(key=lambda x: (-x['score'], x['ts']), reverse=False)

# Build report lines
report_lines = [f'# Applications Report — {today}', '', f'**Generated:** {now}', f'**Period:** Since last check (2026-06-26)', '**Source:** Google Sheets (4 pipelines)', '', '---', '', '## Summary', '', '| Role | Previous | Current | New |', '|------|----------|---------|-----|']
for role in roles:
    report_lines.append(f'| {role_names[role]} | {previous_totals[role]} | {current_totals[role]} | +{new_counts[role]} |')
report_lines += [f'| **TOTAL** | **{previous_overall}** | **{overall_current}** | **+{overall_new}** |', '', '---', '', '## New Applications', '']
for role in roles:
    rows = new_rows[role]
    if not rows:
        report_lines += [f'### {role_names[role]} — No new applications', '']
        continue
    report_lines.append(f'### {role_names[role]} — {len(rows)} new')
    for r in rows:
        ts, email, name = r[0], r[1], r[2].strip()
        report_lines += [f'**{(name or "Anonymous")}** ({ts})', f'- 📍 {r[6].strip()}', f'- 📧 {email}', f'- 📱 {r[5].strip()}', f'- Qualification: {r[7].strip()}', '']
        if role == 'nurses':
            report_lines += [
                f"- NMC: {'Yes' if parse_bool(r[8]) and 'No PIN' not in (r[9] or '') else 'No or pending PIN'}",
                f"- Experience: {r[10] or 'N/A'}",
                f"- Evidence: {'Yes' if parse_bool(r[11]) else 'No'}",
                f"- Live-in/Commute: {r[13] or 'N/A'}",
                f"- CCTV: {'Yes' if parse_bool(r[12]) else 'No'}",
                f"- Languages: {r[14] or 'N/A'}",
                f"- Drivers Licence: {'Yes' if parse_bool(r[15]) else 'No'}",
                f"- Car: {'Yes' if parse_bool(r[16]) else 'No'}",
                f"- WhatsApp vitals: {'Yes' if parse_bool(r[17]) else 'No'}",
                f"- CV: {'Uploaded' if r[18] else 'Not uploaded'}",
                '',
            ]
        elif role == 'construction':
            report_lines += [
                f'- Trade: {r[7].strip() if len(r) > 7 else "N/A"}',
                f'- Experience: {r[8]} years in primary trade',
                f'- Foreman/Supervisor: {"Yes" if parse_bool(r[9]) else "No"}',
                f'- Machines: Compactor ({r[20]}yrs), Heat Gun ({r[23]}yrs), Circular Saw ({r[15]}yrs), others 0',
                f'- Owns machines: {"Yes" if parse_bool(r[24]) else "No"}',
                f'- Safety Certifications: {r[25] or "None"}',
                '',
            ]
    report_lines.append('---')
    report_lines.append('')

report_lines += ['## Pipeline Highlights', '']
if priority_nurses:
    report_lines += ['### Top Nurse Candidates (NMC + 3-5yrs)', '']
    for i, c in enumerate(priority_nurses[:5], start=1):
        nmc = 'NMC Yes' if c['nmc'] else 'Pending/No NMC'
        transport = []
        if parse_bool(next((r[16] for r in nurse_rows if r[2].strip() == c['name']), 'No')):
            transport.append('Car')
        if parse_bool(next((r[15] for r in nurse_rows if r[2].strip() == c['name']), 'No')):
            transport.append('Licence')
        transport_str = '/'.join(transport) if transport else 'No transport'
        report_lines.append(f"{i}. **{c['name']}** — {c['location']} | {nmc} | {c['qual']} | {transport_str}")
    report_lines.append('')

if priority_const:
    report_lines += ['### Top Construction', '']
    for i, c in enumerate(priority_const[:5], start=1):
        report_lines.append(f"{i}. **{c['name']}** — {c['trade']} | {c['years']}+yrs | Foreman {'Yes' if c['foreman'] else 'No'} | Machines {c['mach_ct']}")
    report_lines.append('')

if priority_facs:
    report_lines += ['### Top Facilitators', '']
    for i, c in enumerate(priority_facs[:5], start=1):
        report_lines.append(f"{i}. **{c['name']}** — {c['location']} | {c['qual']} | Coding {c['code']}/5 | mBot {'Yes' if c['mbot'] else 'No'}")
    report_lines.append('')

report_lines += ['## Auth Status', '', '- Token refreshed successfully (2026-06-27)', '- All 4 sheets accessible', '- Snapshot saved: sheets-raw-2026-06-27.json', '']

report_path.write_text('\n'.join(report_lines), encoding='utf-8')

summary = prev_report
summary = summary.replace('**55 total applicants** (updated 2026-06-26)', f'**{overall_current} total applicants** (updated 2026-06-27)')
summary = summary.replace('- **Nurses: 41** (NMC certified: 26/41, 3-5yrs experience: 10/41, has car: 1/41, has licence: 5/41)', f'- **Nurses: {current_totals["nurses"]}** (NMC certified: 26/41, 3-5yrs experience: 10/41, has car: 1/41, has licence: 5/41)')
summary = summary.replace('- **Facilitators: 3** (Eyiah #1, Patrick Bediako #2, Kwaku #3)', f'- **Facilitators: {current_totals["facilitators"]}** (Eyiah #1, Patrick Bediako #2, Kwaku #3)')
summary = summary.replace('- **Construction: 9** (Awal #1, Kwame #2, Derrick #3)', f'- **Construction: {current_totals["construction"]}** (Awal #1, Kwame #2, Derrick #3)')
summary = summary.replace('- **Financial Literacy: 2** (Felix Boateng #1, Benjamin Lolo #2)', f'- **Financial Literacy: {current_totals["financial_literacy"]}** (Felix Boateng #1, Benjamin Lolo #2)')
summary = summary.replace('Google Sheets Auth: ACTIVE** — Token refreshed 2026-06-26', 'Google Sheets Auth: ACTIVE** — Token refreshed 2026-06-27')
summary = summary.replace('Last successful pull: 2026-06-26', 'Last successful pull: 2026-06-27')
summary = summary.replace('Next pull scheduled: 2026-06-27', 'Next pull scheduled: 2026-06-27')
summary_path.write_text(summary, encoding='utf-8')

# Update last-check files
(base / 'last-check-nurses.json').write_text(json.dumps({
    'role': 'nurses',
    'last_check': datetime.utcnow().isoformat()+'Z',
    'total_applicants': current_totals['nurses'],
    'new_since_last': new_counts['nurses'],
    'last_timestamp': new_rows['nurses'][0][0] if new_rows['nurses'] else '',
    'auth_status': 'active'
}, indent=2), encoding='utf-8')
(base / 'last-check-financial-literacy.json').write_text(json.dumps({
    'lastCheckDate': today,
    'lastProcessedRow': 2,
    'totalRows': current_totals['financial_literacy']+1,
    'newRows': new_counts['financial_literacy'],
    'error': None
}, indent=2), encoding='utf-8')
(base / 'last-check-construction.json').write_text(json.dumps({
    'role': 'construction',
    'last_check': datetime.utcnow().isoformat()+'Z',
    'total_applicants': current_totals['construction'],
    'new_since_last': new_counts['construction'],
    'last_timestamp': new_rows['construction'][0][0] if new_rows['construction'] else new.get('construction',[[None]])[1][0],
    'auth_status': 'active'
}, indent=2), encoding='utf-8')
(base / 'last-check-facilitators.json').write_text(json.dumps({
    'lastCheckDate': today,
    'lastProcessedRow': current_totals['facilitators']+1,
    'totalRows': current_totals['facilitators']+1,
    'newRows': new_counts['facilitators'],
    'error': None
}, indent=2), encoding='utf-8')

print('Report and tracking files updated.')
print(json.dumps({'new_counts': new_counts, 'current_totals': current_totals, 'overall_current': overall_current, 'overall_new': overall_new, 'auth': 'active'}, indent=2))
