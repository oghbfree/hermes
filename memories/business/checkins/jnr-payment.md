# Jnr Payment Reminder Log

## 2026-06-13 (Friday)

**Status:** ❌ NOT SENT  
**Channel:** WhatsApp  
**Contact:** Jnr  
**Reason:** WhatsApp bridge remains offline. `hermes send --to whatsapp:...` returns error 503: "Not connected to WhatsApp". Session directory `~/.hermes/whatsapp/session` is empty; no active authentication/session files (creds.json) present. Bridge has not been re-paired since late April/early May.

**Failure history:**
- 2026-05-19 — not sent (bridge down)
- 2026-05-28 — not sent (bridge down)
- 2026-05-31 — WhatsApp tool unavailable
- 2026-06-01 — provider/connection error
- 2026-06-04 — not sent (bridge down)
- 2026-06-07 — not sent (bridge down)
- 2026-06-13 — not sent (bridge down)

**Outstanding amount/enquiry summary:**
- Estate insights note: "told jnr 18k on thurs in jan, nov not paid"
- No current invoice/outstanding clearly quantified in this run; outstanding payment context carried from prior runs.

**Artifacts:** Cron output saved by Hermes cron runner under `~/.hermes/cron/output/46bdb084c174/`.

**Required remediation:** H must re-authenticate the WhatsApp bridge via QR scan from Windows before any of the 8+ WhatsApp-dependent cron jobs (`jnr-payment-reminder`, `sammy-morning-check`, `john-field-check`, `checkin-dad`, `checkin-mum`, `ebony-goodnight`, `kanzoni-tuesday-check`, `janet-friday-checkin`) can deliver again.

---

## 2026-06-07 (Sunday)

**Status:** ❌ NOT SENT  
**Channel:** WhatsApp  
**Contact:** Jnr  
**Reason:** WhatsApp bridge remains offline. Session directory `~/.hermes/whatsapp/session` is empty; no active authentication/session files are present. Bridge has not been re-paired since late April/early May.

**Failure history:**
- 2026-05-19 — not sent (bridge down)
- 2026-05-28 — not sent (bridge down)
- 2026-05-31 — WhatsApp tool unavailable
- 2026-06-01 — provider/connection error
- 2026-06-04 — not sent (bridge down)
- 2026-06-07 — not sent (bridge down)

**Outstanding amount/enquiry summary:**
- Estate insights note: "told jnr 18k on thurs in jan, nov not paid"
- No current invoice/outstanding clearly quantified in this run; outstanding payment context carried from prior runs.

**Artifacts:** Cron output saved by Hermes cron runner under `~/.hermes/cron/output/46bdb084c174/`.

**Required remediation:** H must re-authenticate the WhatsApp bridge via QR scan from Windows before any of the 8+ WhatsApp-dependent cron jobs (`jnr-payment-reminder`, `sammy-morning-check`, `john-field-check`, `checkin-dad`, `checkin-mum`, `ebony-goodnight`, `kanzoni-tuesday-check`, `janet-friday-checkin`) can deliver again.