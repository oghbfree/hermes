# Hermes Environment Notes

- **Hermes Desktop app** (`com.nousresearch.hermes.setup` in `AppData\Local`) is an Electron wrapper — it does NOT have its own Hermes instance
- Both Desktop and the gateway share `C:\Users\User\.hermes\`
- Cron jobs, skills, memories, sessions are all single-source — no mirroring needed
