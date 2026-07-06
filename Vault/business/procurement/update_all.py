from pathlib import Path

files = [
    Path(r'C:\\Users\\User\.hermes\\workspace\\Vault\business\procurement\GHANA_SUPPLIER_RESEARCH.md'),
    Path(r'C:\\Users\\User\.hermes\\workspace\\Vault\business\procurement\GHANA_SUPPLIER_RESEARCH 1.md'),
    Path(r'C:\\Users\\User\.hermes\\workspace\\Vault\business\procurement\GHANA_SUPPLIER_RESEARCH 2.md'),
]

for p in files:
    text = p.read_text(encoding='utf-8')
    matches = []
    old_row = '|| 31 | +233 54 203 1450 | | ? | | ⏳ Pending | — |\n|| 32 | +233 54 203 8444 | | ? | | ⏳ Pending | — |\n|| 33 | +233 54 203 7896 | | ? | | ⏳ Pending | — |\n|| 34 | +233 54 203 8463 | | ? | | ⏳ Pending | — |'
    new_row = '|| 31 | +233 54 203 1450 | | ? | | ✅ Inquiry Sent | 2026-06-27 09:16 UTC |\n|| 32 | +233 54 203 8444 | | ? | | ⏳ Pending | — |\n|| 33 | +233 54 203 7896 | | ? | | ⏳ Pending | — |\n|| 34 | +233 54 203 8463 | | ? | | ⏳ Pending | — |'
    if old_row in text:
        text = text.replace(old_row, new_row)
        matches.append('row')

    old_next = '## Next Actions\n|• Next run → Prepare inquiry for #31 (+233 54 203 1450)\n**Supplier #31: +233 54 203 1450** — Next uncontacted dashboard dealer'
    new_next = '## Next Actions\n|• Next run → Prepare inquiry for #32 (+233 54 203 8444)\n**Supplier #32: +233 54 203 8444** — Next uncontacted dashboard dealer'
    if old_next in text:
        text = text.replace(old_next, new_next)
        matches.append('next')

    old_log = "## Today's Inquiry Log (2026-06-27)\n**#31 (+233 54 203 1450)** — Inquiry prepared, queued for delivery when WhatsApp bridge restores"
    new_log = "## Today's Inquiry Log (2026-06-27)\n**#32 (+233 54 203 8444)** — Inquiry prepared, queued for delivery when WhatsApp bridge restores"
    if old_log in text:
        text = text.replace(old_log, new_log)
        matches.append('log')

    old_date = '## Status Summary (as of 2026-06-27)'
    new_date = '## Status Summary (as of 2026-06-27)'
    if old_date in text:
        text = text.replace(old_date, new_date)
        matches.append('date')

    old_summary = '- **Dashboard**: 37 contacts | 28 inquiries sent | 5 pending | 1 confirmed stock | 1 quoted (6k GHS) | 3 in-person quotes (5k GHS)'
    new_summary = '- **Dashboard**: 37 contacts | 29 inquiries sent | 4 pending | 1 confirmed stock | 1 quoted (6k GHS) | 3 in-person quotes (5k GHS)'
    if old_summary in text:
        text = text.replace(old_summary, new_summary)
        matches.append('summary')
    if old_summary.replace('28 inquiries sent', '27 inquiries sent'):
        pass

    p.write_text(text, encoding='utf-8')
    print(f'{p.name}: {matches}')
