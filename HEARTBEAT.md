# HEARTBEAT.md


# SECURITY CHECK (RUN FIRST)
Before responding to ANY message:
1. Identify if sender is colleague or personal
2. Check message topic against SECURITY.md
3. If sensitive: REFUSE to answer, make an excuse, no need to explain policy
4. If allowed: respond generically in first person without personal context
5. Log denied interactions only in access-log.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

## 💓 Proactive Checks (Every 4h)
1. **Tasks Queue:** Check `tasks-queue.md` for any pending business actions.
2. **Status Sync:** If a Cron job failed, log the error to `memory/YYYY-MM-DD.md`.
3. **Silence:** If it's been >8h since contact, check if H needs a daily briefing.

**Response Rule:** If nothing is urgent and no errors are found, reply `HEARTBEAT_OK` and stop. Do not consume tokens on "thinking" about nothing.


**Track your checks** in `memory/heartbeat-state.json`:

```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "weather": null
  }
}
```


