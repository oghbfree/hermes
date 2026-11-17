# PERMANENT BUSINESS BROWSER — setup & operations
_Built 16/11/26. One Chrome instance, one profile, all business channels, self-healing._

---

## What this replaces

The old setup had a launcher (`start_persistent_browser.bat`) that fired **once at logon** and
nothing more. It also used `--no-startup-window` and pinned CDP to `:64365`. Result: the browser
died and stayed dead, and four scripts hardcoded to `:64365` failed silently while the browser was
perfectly alive on a different port.

## Components

| File (`profiles/sat-nav/scripts/`) | Role |
|---|---|
| `cdp_port.py` | **Single source of truth for the CDP port.** Reads `<profile>/DevToolsActivePort` first, then probes. Never hardcode a port again. |
| `permanent_browser.py` | Launcher/ensurer. Idempotent — if CDP is live it does NOT relaunch, it only adds missing tabs. `--status`, `--restart`, `--prune`. |
| `browser_watchdog.py` | Supervisor loop. Checks every 60s, relaunches within ~60s of a death, re-opens missing tabs every 10 min. Crash-loop guarded (max 4 restarts/30min, then 10-min backoff). |
| `browser_login_status.py` | Reports which channels are signed in. Read-only. |
| `Startup\hermes_browser_watchdog.vbs` | Auto-starts the watchdog hidden at logon (no admin needed). |

The old `Hermes Persistent Browser.bat` was **retired from Startup** (kept in `scripts/` as
`Hermes Persistent Browser.bat.retired_from_startup`) so it cannot race the watchdog.

## Channels (8)

WhatsApp Web · Facebook Marketplace · Jiji · Instagram · Meta Business Suite · TikTok ·
LinkedIn · YouTube

Profile: `C:\Users\User\AppData\Local\hermes\browser-profile\chrome` — **same profile every time**,
so all logins persist across restarts.

## Daily commands

```bash
cd C:/Users/User/AppData/Local/hermes/profiles/sat-nav/scripts

python cdp_port.py                 # what port is the browser on?
python permanent_browser.py        # ensure browser + all 8 tabs (safe to run anytime)
python permanent_browser.py --status    # report only
python permanent_browser.py --restart   # kill the profile's Chrome and relaunch clean
python permanent_browser.py --prune     # close duplicate/junk tabs
python browser_login_status.py     # which channels are signed in
```

Log: `cache/scratch/permanent_browser.log`

## Verified 16/11/26

- Cold start from a fully killed browser: **recovered in ~10s**, came up on its **preferred port 64365**, 8/8 channels.
- **Auto-recovery proven:** browser killed externally → watchdog detected and relaunched within ~80s, unaided.
- Duplicate tabs from Chrome's session restore are pruned automatically (went 20 tabs → 8).
- Logins survived a full kill/relaunch: WhatsApp showed 13 unread, Facebook 3 notifications, Meta Business Suite business_id intact, Jiji live.
- `wa_meta_monitor.py` / `wa_meta_probe.py` / `wa_meta_watcher.py` patched to resolve the live port instead of assuming 64365.

## Auth state

| Channel | State |
|---|---|
| WhatsApp | ✅ signed in |
| Facebook | ✅ signed in |
| Meta Business Suite | ✅ signed in (business_id 1099498076173058) |
| Jiji | ✅ signed in |
| LinkedIn | ✅ signed in |
| YouTube | ✅ signed in |
| **Instagram** | ❌ **needs one manual login** — sits on "Log into Instagram" |
| **TikTok** | ⚠️ **HTTP 403 "Access denied"** — not a login problem, access is being refused for this network/IP. Likely needs a different route/VPN; signing in will not fix it. |

**The browser keeps sessions alive; it cannot log in for you.** Sign in once in that window and it
persists.

## Known gotchas (learned the hard way)

1. **Never hardcode the CDP port.** Chrome silently falls back to a random port when the requested
   one is taken (TIME_WAIT counts). Always call `cdp_port.py`.
2. **`--no-startup-window` can leave Chrome window-less and exiting** — removed.
3. **Do not pass the Chrome path inside the argument list.** Doing so made Chrome parse
   `C:\Program Files\...` fragments as URLs and open junk `file:///C:/Program` tabs.
4. **Chrome restores the previous session asynchronously after launch**, re-adding duplicate tabs
   — hence the second prune pass ~8s after launch.
5. **A stale Chrome holding the profile without CDP is unrecoverable** — it must be killed and
   replaced (`--restart`). The watchdog detects and does this automatically.
6. **Scheduled Task registration needs admin** (`Register-ScheduledTask` → Access denied), which is
   why the watchdog runs from the Startup folder instead.
