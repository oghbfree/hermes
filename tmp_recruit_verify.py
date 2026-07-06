
import json
from pathlib import Path

paths = [Path(r'C:\Users\User\.hermes\workspace\Vault\jobs\sheets-raw-2026-06-27.json'),
         Path(r'C:\Users\User\.hermes\workspace\Vault\jobs\APPLICATIONS-REPORT-2026-06-27.md'),
         Path(r'C:\Users\User\.hermes\workspace\Vault\jobs\RECRUITMENT_SUMMARY.md')]
json_paths = [
    Path(r'C:\Users\User\.hermes\workspace\Vault\jobs\last-check-nurses.json'),
    Path(r'C:\Users\User\.hermes\workspace\Vault\jobs\last-check-financial-literacy.json'),
    Path(r'C:\Users\User\.hermes\workspace\Vault\jobs\last-check-construction.json'),
    Path(r'C:\Users\User\.hermes\workspace\Vault\jobs\last-check-facilitators.json'),
]
expected = ['updated 2026-06-27', 'Token refreshed successfully (2026-06-27)']
errors = []
for p in paths + json_paths:
    if not p.exists():
        errors.append(f'missing {p}')
        continue
    if p.suffix == '.json':
        try:
            json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            errors.append(f'{p}: {e}')
if errors:
    raise SystemExit('VERIFY FAIL: ' + '; '.join(errors))
print('VERIFY OK')
