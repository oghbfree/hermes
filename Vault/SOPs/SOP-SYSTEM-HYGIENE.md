---
title: SOP — System Hygiene (Backups, Storage, Credentials)
date: 2026-10-03
tags: [sop, system]
---

# SOP — System Hygiene

## Backups
- Daily automated vault/system backups exist under `~/.hermes/backups/` — verify `latest/` is fresh (<24h) after any big change.
- Before ANY bulk delete: backup → list exactly what will be deleted → H approval → delete → verify live store intact.
- Deleted-stale pattern (11 Aug 26): stale cron stores removed only after backup + explicit "yes".

## Storage
- Watch for: recursive backup copies, stale DB backups, orphan files. Run recovery passes when disk grows.
- Temp scripts (`scan_*.py`, `make_*.py`) get deleted after use; outputs land in the vault, not home dir.

## Credentials
- Keys live in `.env` / profile dirs only. If a secret ever appears in chat/logs/files → treat as compromised, rotate, scrub with `***` (the vision-key precedent).
- Bot token revoked? Report to H, don't attempt gateway surgery (forbidden: gateway stop/start/restart).

## Cron
- Live store: `AppData/Local/hermes/cron/` only. Stale stores = deletion candidates after backup + approval.
