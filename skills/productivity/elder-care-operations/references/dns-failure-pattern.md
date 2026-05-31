# DNS Resolution Failure Pattern — Telegram API

**Date observed:** May 18, 2026 at 19:00 UTC+1

## Symptoms
- Cron jobs with `last_status: "error"` and `last_error: "RuntimeError: Connection error."`
- `last_delivery_error: "delivery error: Telegram send failed: httpx.ConnectError: [Errno 11001] getaddrinfo failed"`
- Affects ALL Telegram deliveries at the same time (not job-specific)
- Both `mum-health-evening` (topic 4) and `health-check-evening` (topic 2) failed simultaneously

## Root Cause
The Windows host could not resolve the Telegram API domain (`api.telegram.org`) at the time of execution. This is a DNS resolution failure, not a Telegram API issue or a cron configuration issue.

## Diagnosis Steps
1. Check if the failure was transient (single occurrence) or persistent (recurring)
2. If recurring: check the host's DNS settings — `ipconfig /all` for DNS server config
3. Try switching to a public DNS (8.8.8.8, 1.1.1.1) if ISP DNS is unreliable
4. Check router DNS settings
5. Verify no firewall or proxy is blocking DNS resolution

## Affected Jobs (May 18, 2026)
- `mum-health-evening` (7ffb54b79331) — 19:00 → topic 4
- `health-check-evening` (c4818bab761b) — 19:00 → topic 2

## Mitigation
- The `security-policy-check` cron (73f447bae072) runs every 6 hours and can detect DNS issues in its channel integrity section
- If DNS failures are detected, the audit should flag them as a WARN under Channel Integrity
- Consider adding a DNS health check to the security audit script
