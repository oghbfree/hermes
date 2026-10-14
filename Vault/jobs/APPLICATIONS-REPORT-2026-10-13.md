# Applications Report — 2026-10-13

## Run Summary
Cron: job-applications-check (2026-10-13 12:18 GMT).

## Token & Fetch
- Google OAuth token was expired (since 10-12). Ran `refresh_token.py` → SUCCESS, token refreshed.
- Ran `fetch_all_sheets.py` → wrote `sheets-raw-2026-10-13.json`.

## Diff (baseline = last reported pull 2026-10-12)
- **Nurses: +1 new** | construction: 0 new | facilitators: 0 new | financial_literacy: 0 new
- 1 new application this pull.

## New Applicant (Nurses)
- **Elizabeth Owusuaa** (12/10/2026 15:01:19) — Ayimensah. Diploma in Montessori Early Childhood Ed, 3yrs teaching. NMC: No | exp: 0-2yrs | Commute | CCTV: Yes | No car, No driver's licence | CV uploaded.
- **Below nurse priority threshold** (requires NMC registered + 3-5yrs + car/licence as priority). Not shortlisted.

## Filtering
- Priority nurse filter (NMC + 3-5yrs): 7 (unchanged). Top: Charlotte Nortey (NMC + car + licence) | Mohammed Shaibu (licence, no car).
- Construction Foreman +6yrs: 8 | Facilitators mBot + coding 4+: 2 | Fin-Lit: 2. All unchanged.

## Totals
- Nurses: 53 (NMC+3-5yrs: 7) | Construction: 13 | Facilitators: 4 | Fin-Lit: 2 | **Total: 72**

## Files Updated
- `APPLICATIONS-REPORT-2026-10-13.md` (created)
- `last-check-{nurses,construction,facilitators,financial-literacy}.json` (updated to 2026-10-13)
- `RECRUITMENT_SUMMARY.md` (latest pull section + status)

## Telegram
- Delivered to Jobs topic (thread 28, chat -1003784520976) via Bot API.