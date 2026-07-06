from pathlib import Path

p = Path(r'C:\\Users\\User\.hermes\\workspace\\Vault\business\procurement\GHANA_SUPPLIER_RESEARCH.md')
text = p.read_text(encoding='utf-8')

old_row = '|| 30 | +233 54 203 4633 | | ? | | ⏳ Pending | — |\n|| 31 | +233 54 203 1450 | | ? | | ⏳ Pending | — |\n|| 32 | +233 54 203 8444 | | ? | | ⏳ Pending | — |\n|| 33 | +233 54 203 7896 | | ? | | ⏳ Pending | — |\n|| 34 | +233 54 203 8463 | | ? | | ⏳ Pending | — |'
new_row = '|| 30 | +233 54 203 4633 | | ? | | ✅ Inquiry Sent | 2026-06-27 09:16 UTC |\n|| 31 | +233 54 203 1450 | | ? | | ⏳ Pending | — |\n|| 32 | +233 54 203 8444 | | ? | | ⏳ Pending | — |\n|| 33 | +233 54 203 7896 | | ? | | ⏳ Pending | — |\n|| 34 | +233 54 203 8463 | | ? | | ⏳ Pending | — |'
text = text.replace(old_row, new_row)

old_next = '## Next Actions\n|• Next run → Prepare inquiry for #30 (+233 54 203 4633)\n**Supplier #30: +233 54 203 4633** — Next uncontacted dashboard dealer'
new_next = '## Next Actions\n|• Next run → Prepare inquiry for #31 (+233 54 203 1450)\n**Supplier #31: +233 54 203 1450** — Next uncontacted dashboard dealer'
text = text.replace(old_next, new_next)

old_log = "## Today's Inquiry Log (2026-06-22)\n**#29 (+233 54 203 0706)** — Inquiry prepared, queued for delivery when WhatsApp bridge restores"
new_log = "## Today's Inquiry Log (2026-06-27)\n**#30 (+233 54 203 4633)** — Inquiry prepared, queued for delivery when WhatsApp bridge restores"
text = text.replace(old_log, new_log)

old_date = '## Status Summary (as of 2026-06-22)'
new_date = '## Status Summary (as of 2026-06-27)'
text = text.replace(old_date, new_date)

old_summary = '- **Dashboard**: 37 contacts | 27 inquiries sent | 6 pending | 1 confirmed stock | 1 quoted (6k GHS) | 3 in-person quotes (5k GHS)'
new_summary = '- **Dashboard**: 37 contacts | 28 inquiries sent | 5 pending | 1 confirmed stock | 1 quoted (6k GHS) | 3 in-person quotes (5k GHS)'
text = text.replace(old_summary, new_summary)

p.write_text(text, encoding='utf-8')
print('UPDATED')
