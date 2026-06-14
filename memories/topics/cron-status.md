# Cron Jobs Status

## Connection Error Cluster (May 29)

5 cron jobs failed with `RuntimeError: Connection error` between 00:49-09:01:
- daily-backup
- security-policy-check
- Morning Priority Check-in
- tasks-queue-sync
- cron-status-report

**Cron SLA collapsed:** 96.3% (May 28) → 32.3% (May 29)
**Likely cause:** upstream connectivity/OpenRouter issue

## WhatsApp-Dependent Jobs (Dead Since May 18)

All non-functional due to WhatsApp bridge outage:
- 8+ cron jobs affected
- See [[whatsapp-status]]

## Working Jobs

- Dad health check-ins: operational via Telegram topic 1 (3/3 daily prompts delivered since May 19)
- Morning Priority Check-in: created May 22, asks H for #1 priority at 04:45 BST

## Related

- See also: [[whatsapp-status]], [[backup-status]]
