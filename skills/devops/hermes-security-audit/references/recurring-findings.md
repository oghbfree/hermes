## Bitwarden Integration (added 2026-05-31)

- **Bitwarden Secrets Manager** confirmed active — 15 secrets injected at runtime. See `references/bitwarden-integration.md`.
- `.env` values showing `***` are literal asterisks — NOT recoverable. Must regenerate from source dashboards and re-store in Bitwarden.
- Dashboard port: 9119 (Hermes plugin HTTP server). Kanban API requires browser login first.

## Recurring Findings Tracker

Tracks findings that persist across multiple audit cycles. Escalate priority after 3+ consecutive appearances.

## Active Carry-Forward Findings

| # | Finding | First Seen | Last Seen | Count | Severity | Action Required |
|---|---------|-----------|-----------|-------|----------|-----------------|
| 01 | `.env`, `auth.json`, `google_token.json`, `google_client_secret.json` all 644 (world-readable) | 2026-05-23 | 2026-05-30 | 8+ | 🔴 FAIL | `chmod 600` on all |
| 02 | FAL_KEY duplicated in `.env` with full plaintext value | 2026-05-29 | 2026-05-30 | 2 | 🔴 FAIL | Remove duplicate, rotate key |
| 03 | WhatsApp enabled but fatal (not paired) | 2026-05-29 | 2026-05-30 | 2 | 🟡 WARN | Pair or disable |
| 04 | Discord paused, no token configured, 10+ reconnection failures | 2026-05-29 | 2026-05-30 | 2 | 🟡 WARN | Configure or disable |
| 05 | Ollama `id_ed25519` private key 644 (if exists) | 2026-05-29 | 2026-05-29 | 1 | 🟡 WARN | `chmod 600` |
| 06 | Multiple backup sets contain plaintext credentials | 2026-05-28 | 2026-05-28 | 1 | 🟡 WARN | Rotate or encrypt backups |

## New in 2026-05-30

| # | Finding | Severity | Action Required |
|---|---------|----------|-----------------|
| 07 | Google OAuth token expired (2026-05-28) — gmail, drive, calendar, sheets scopes | 🔴 FAIL | Re-authenticate (`gws auth`) |
| 08 | Unauthorized WhatsApp user `279572927017208@lid` attempted access | 🔴 FAIL | Verify not expected contact |
| 09 | `tirith` security module missing on Windows (30+ spawn failures) | 🟡 WARN | Investigate installation |
| 10 | `redact_pii: false` in config.yaml | 🟡 WARN | Change to `true` |
| 11 | State.db trajectory: 258MB @ ~8MB/day growth; request dumps: 164 files | 🟡 WARN | Add cleanup to nightly-consolidation |
| 12 | Full secrets in 10+ disk locations (see §1m secret-surface map in SKILL.md) | 🔴 FAIL | Migrate to Bitwarden runtime injection (SKILL.md §1h-2) |
| 13 | FAL_KEY fully exposed + duplicated (lines 19-20) — persists since first audit | 🔴 FAIL | Rotate FAL_KEY, remove duplicate line, add to Bitwarden vault |

## New in 2026-05-31

| # | Finding | Severity | Action Required |
|---|---------|----------|-----------------|
| 14 | Bitwarden CLI installed, migration in progress — H's vault confirmed (US cloud) | 🟡 INFO | Complete migration: create BW entries for all 20 .env keys, switch to `bw serve` runtime injection, delete plaintext .env |

## Closed Findings

| # | Finding | Closed | Resolution |
|---|---------|--------|------------|
| — | *(none yet)* | — | — |

## Escalation Rules

- **3+ consecutive FAIL items:** Escalate to "persistent security debt" — add to daily briefing
- **5+ consecutive FAIL items:** Escalate to CRITICAL — immediate manual intervention required
- **Any finding unaddressed for 2 weeks:** Send reminder to Telegram
