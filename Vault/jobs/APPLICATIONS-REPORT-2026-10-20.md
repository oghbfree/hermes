# Applications Report — 2026-10-20

## Run Summary
Cron: job-applications-check (2026-10-20 08:56 GMT).

## Token & Fetch
- Google OAuth token was expired (since 10-19). Ran `refresh_token.py` → SUCCESS, token refreshed.
- Ran `fetch_all_sheets.py` → wrote `sheets-raw-2026-10-20.json`.

## Diff (baseline = last reported pull 2026-10-19)
- **Nurses: 0 new** | construction: 0 new | facilitators: 0 new | financial_literacy: 0 new
- No new applications across any pipeline.

## Filtering
- N/A — no new applicants to screen. Priority counts from live 10-20 snapshot, unchanged:
  - Nurses NMC+3-5yrs: 7 (top: Charlotte Nortey — NMC + car + licence, only applicant with all three)
  - Construction Foreman +6yrs: 7 (Awal, Kwame Odoom, Derrick, Amane John, Amuzu, Woedzagbagba, Eric Otoo)
  - Facilitators mBot + coding 4+: 2 (Eyiah Michael Osardu, Patrick Selorm Bediako)
  - Fin-Lit: 2 (Felix Boateng, Benjamin Lolo)

## Totals
- Nurses: 53 (NMC+3-5yrs: 7) | Construction: 13 | Facilitators: 4 | Fin-Lit: 2 | **Total: 72**
- Priority counts unchanged (7/7/2/2).

## Files Updated
- `APPLICATIONS-REPORT-2026-10-20.md` (created)
- `last-check-{nurses,construction,facilitators,financial-literacy}.json` (updated to 2026-10-20)
- `RECRUITMENT_SUMMARY.md` (latest pull section + status)

## Verification
- last-check JSONs valid; totals re-confirmed nurses 53/0 new, construction 13/0, facilitators 4/0, fin-lit 2/0; report + snapshot present; summary greps consistent.

## Telegram
- Delivered to Jobs topic (thread 28, chat -1003784520976).