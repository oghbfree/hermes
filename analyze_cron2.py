import json
from datetime import datetime
from pathlib import Path

jobs_data = [
    {"id": "bc929d4338f1", "name": "Evening habit reflect", "schedule": "0 19 * * *", "deliver": "local", "last_run": "2026-07-13T19:00:51.742852+01:00", "status": "ok", "error": None},
    {"id": "96fa9febc949", "name": "tasks-queue-sync", "schedule": "0 9 * * *", "deliver": "origin", "last_run": "2026-07-13T09:01:44.324352+01:00", "status": "ok", "error": None},
    {"id": "7c8fb59db4dd", "name": "brain-dump-parser", "schedule": "0 8,12,18 * * *", "deliver": "telegram:-1003784520976:8", "last_run": "2026-07-13T18:00:35.796065+01:00", "status": "error", "error": "HTTP 429: Rate limit exceeded: free-models-per-day-high-balance"},
    {"id": "1efc20613995", "name": "tasks-md-to-kanban", "schedule": "0 10 * * *", "deliver": "origin", "last_run": "2026-07-13T10:09:21.847571+01:00", "status": "ok", "error": None},
    {"id": "1cf75a0caf85", "name": "sunday-content-engine", "schedule": "0 20 * * 0", "deliver": "telegram:-1003784520976:26", "last_run": "2026-07-13T00:39:49.963295+01:00", "status": "ok", "error": None},
    {"id": "a52b43d3ec6e", "name": "saturday-content-performance", "schedule": "11 9 * * 6", "deliver": "telegram:-1003784520976:26", "last_run": "2026-07-11T09:16:52.393059+01:00", "status": "ok", "error": None},
    {"id": "3b593315ac1c", "name": "mum-health-morning", "schedule": "4 8 * * *", "deliver": "local", "last_run": "2026-07-14T22:20:21.306106+01:00", "status": "error", "error": "TimeoutError: Cron job idle for 41631s (limit 600s) — last activity: API error recovery (attempt 1/3)"},
    {"id": "fb07221a65b8", "name": "mum-health-afternoon", "schedule": "0 13 * * *", "deliver": "local", "last_run": "2026-07-14T22:20:55.121157+01:00", "status": "ok", "error": None},
    {"id": "6a95ab36d017", "name": "mum-health-evening", "schedule": "0 19 * * *", "deliver": "local", "last_run": "2026-07-13T19:00:36.751115+01:00", "status": "error", "error": "HTTP 429: Rate limit exceeded: free-models-per-day-high-balance"},
    {"id": "e5be79ac5f9a", "name": "health-check-morning", "schedule": "4 8 * * *", "deliver": "local", "last_run": "2026-07-13T08:11:28.722593+01:00", "status": "ok", "error": None},
    {"id": "1811327d1a56", "name": "health-check-afternoon", "schedule": "0 13 * * *", "deliver": "local", "last_run": "2026-07-13T13:00:33.804056+01:00", "status": "error", "error": "HTTP 429: Rate limit exceeded: free-models-per-day-high-balance"},
    {"id": "42d142d01603", "name": "health-check-evening", "schedule": "0 19 * * *", "deliver": "local", "last_run": "2026-07-13T19:01:01.967236+01:00", "status": "error", "error": "HTTP 429: Rate limit exceeded: free-models-per-day-high-balance"},
    {"id": "c918124458f7", "name": "mum-health-weekly-review", "schedule": "6 9 * * 0", "deliver": "telegram:-1003784520976:4", "last_run": "2026-07-12T09:07:08.945995+01:00", "status": "ok", "error": None},
    {"id": "001aa6093049", "name": "weekly-learning-review", "schedule": "13 9 * * 1", "deliver": "origin", "last_run": "2026-07-13T09:25:32.949583+01:00", "status": "ok", "error": None},
    {"id": "9fc966ea5d04", "name": "monthly-evolution", "schedule": "21 9 1 * *", "deliver": "origin", "last_run": "2026-07-01T09:44:03.446753+01:00", "status": "ok", "error": None},
    {"id": "d0298643f6d6", "name": "ghana-dashboard-inquiry", "schedule": "16 9 * * 1-6", "deliver": "origin", "last_run": "2026-07-13T09:16:09.165767+01:00", "status": "ok", "error": None},
    {"id": "1b7107630fe3", "name": "security-policy-check", "schedule": "4 */6 * * *", "deliver": "telegram:-1003784520976:20", "last_run": "2026-07-14T06:08:34.213092+01:00", "status": "ok", "error": None},
    {"id": "586aebcd5e57", "name": "daily-backup", "schedule": "3 23 * * *", "deliver": "origin", "last_run": "2026-07-13T23:03:45.315099+01:00", "status": "error", "error": "HTTP 429: Rate limit exceeded: free-models-per-day-high-balance"},
    {"id": "2769dd3ed4e7", "name": "cron-status-report", "schedule": "0 9 * * *", "deliver": "origin", "last_run": "2026-07-13T09:02:52.347993+01:00", "status": "ok", "error": None},
    {"id": "a3cdfceac0c9", "name": "github-memory-backup", "schedule": "2 23 * * 0", "deliver": "origin", "last_run": "2026-07-13T00:31:29.842022+01:00", "status": "ok", "error": None},
    {"id": "20e6fc5fe28c", "name": "nightly-consolidation", "schedule": "0 3 * * *", "deliver": "telegram:-1003784520976:20", "last_run": "2026-07-14T03:04:31.355190+01:00", "status": "ok", "error": None},
    {"id": "2e2d1d6ece88", "name": "job-applications-check", "schedule": "0 8 * * *", "deliver": "telegram:-1003784520976:28", "last_run": "2026-07-13T08:06:26.669533+01:00", "status": "ok", "error": None},
    {"id": "c3db50f4f9af", "name": "checkin-mum", "schedule": "18 10 * * 0,3", "deliver": "origin", "last_run": "2026-07-12T10:21:22.051185+01:00", "status": "ok", "error": None},
    {"id": "f21f8326c44b", "name": "checkin-dad", "schedule": "4 10 * * 0,4", "deliver": "origin", "last_run": "2026-07-12T10:06:47.103037+01:00", "status": "ok", "error": None},
    {"id": "e7c051acc8ce", "name": "kanzoni-tuesday-check", "schedule": "7 7 * * 2", "deliver": "origin", "last_run": "2026-07-07T07:12:47.401783+01:00", "status": "ok", "error": None},
    {"id": "0a3172b06d2a", "name": "sammy-morning-check", "schedule": "2 7 * * 1-6", "deliver": "origin", "last_run": "2026-07-13T07:05:09.860829+01:00", "status": "ok", "error": None},
    {"id": "f67697a2dfb7", "name": "john-field-check", "schedule": "2 8 * * 1-5", "deliver": "origin", "last_run": "2026-07-13T08:02:11.773488+01:00", "status": "ok", "error": None},
    {"id": "5c3fdb74e365", "name": "ebony-goodnight", "schedule": "4 22 * * *", "deliver": "origin", "last_run": "2026-07-13T22:04:43.580851+01:00", "status": "error", "error": "HTTP 429: Rate limit exceeded: free-models-per-day-high-balance"},
    {"id": "4ff54e93664b", "name": "jnr-payment-reminder", "schedule": "5 10 */3 * *", "deliver": "origin", "last_run": "2026-07-13T10:11:48.145794+01:00", "status": "ok", "error": None},
    {"id": "16c8a6f32eb5", "name": "dad-health-weekly-review", "schedule": "30 9 * * 0", "deliver": "telegram:-1003784520976:16", "last_run": "2026-07-12T09:36:41.640865+01:00", "status": "ok", "error": None},
    {"id": "1505fd537513", "name": "Morning Priority Check-in", "schedule": "45 6 * * *", "deliver": "origin", "last_run": "2026-07-13T06:47:54.728660+01:00", "status": "ok", "error": None},
    {"id": "e0e77e600e81", "name": "Fluid CC Payment Reminder", "schedule": "0 10 15 * *", "deliver": "origin", "last_run": None, "status": "never_run", "error": None},
    {"id": "5d80f08b4d6b", "name": "2Real — Daily Operations Check", "schedule": "0 9 * * *", "deliver": "origin", "last_run": "2026-07-13T09:03:14.275142+01:00", "status": "ok", "error": None},
    {"id": "82544c38ad63", "name": "2Real — Inventory Auto-Sync", "schedule": "0 */2 * * *", "deliver": "origin", "last_run": "2026-07-14T06:00:37.105656+01:00", "status": "ok", "error": None},
    {"id": "5f6fafe0aba8", "name": "Dad — 3-Day Condition & Wellbeing Check", "schedule": "0 10 */3 * *", "deliver": "telegram:-1003784520976:16", "last_run": "2026-07-13T10:01:36.569382+01:00", "status": "ok", "error": None},
    {"id": "4f223316a340", "name": "h-health-weekly-review", "schedule": "6 9 * * 0", "deliver": "telegram:-1003784520976:2", "last_run": "2026-07-12T09:08:49.094882+01:00", "status": "ok", "error": None},
    {"id": "f9f90bd47965", "name": "Jiji Ghana auto-reply (computer-use)", "schedule": "*/5 * * * *", "deliver": "origin", "last_run": "2026-07-14T22:20:57.379530+01:00", "status": "error", "error": "Model drift: nvidia/nemotron-3-super-120b-a12b:free -> nvidia/nemotron-3-ultra-550b-a55b:free (unpinned)"},
    {"id": "38eaa5d0ada1", "name": "Jiji Ghana login computer-use", "schedule": "*/10 * * * *", "deliver": "origin", "last_run": "2026-07-14T22:20:57.445023+01:00", "status": "error", "error": "Model drift: nvidia/nemotron-3-super-120b-a12b:free -> nvidia/nemotron-3-ultra-550b-a55b:free (unpinned)"},
    {"id": "fa1743e811ee", "name": "Market Seller Daily Briefing - 4:30 AM", "schedule": "30 4 * * *", "deliver": "telegram:-1003784520976:10", "last_run": "2026-07-14T04:34:23.897075+01:00", "status": "ok", "error": None},
    {"id": "0ef160b1c270", "name": "Daily Marketplace Monitor", "schedule": "0 7 * * *", "deliver": "local", "last_run": "2026-07-13T10:15:21.784675+01:00", "status": "error", "error": "HTTP 429: Rate limit exceeded: free-models-per-day-high-balance"},
]

total_jobs = len(jobs_data)
active_jobs = sum(1 for j in jobs_data if j['status'] != 'never_run')
ok_jobs = sum(1 for j in jobs_data if j['status'] == 'ok')
error_jobs = sum(1 for j in jobs_data if j['status'] == 'error')
never_run = sum(1 for j in jobs_data if j['status'] == 'never_run')

# 24h window: July 13 00:00 to July 14 23:59 (the reporting period)
cutoff = datetime(2026, 7, 13, 0, 0, 0)
end_cutoff = datetime(2026, 7, 14, 23, 59, 59)
jobs_24h = []
for j in jobs_data:
    if j['last_run']:
        try:
            run_time = datetime.fromisoformat(j['last_run'].replace('Z', '+00:00'))
            if cutoff <= run_time <= end_cutoff:
                jobs_24h.append(j)
        except:
            pass

ok_24h = sum(1 for j in jobs_24h if j['status'] == 'ok')
error_24h = sum(1 for j in jobs_24h if j['status'] == 'error')

print(f"Total jobs: {total_jobs}")
print(f"Active: {active_jobs}")
print(f"OK: {ok_jobs}")
print(f"Error: {error_jobs}")
print(f"Never run: {never_run}")
print(f"24h runs: {len(jobs_24h)} (OK: {ok_24h}, Error: {error_24h})")
if jobs_24h:
    print(f"24h Success rate: {ok_24h}/{len(jobs_24h)} = {ok_24h/len(jobs_24h)*100:.0f}%")

# Error breakdown
error_types = {}
for j in jobs_data:
    if j['status'] == 'error':
        etype = j['error'].split(':')[0] if ':' in j['error'] else j['error'][:50]
        error_types[etype] = error_types.get(etype, 0) + 1

print("\nError breakdown:")
for etype, count in sorted(error_types.items(), key=lambda x: -x[1]):
    print(f"  {etype}: {count}")

print("\nJobs with errors:")
for j in jobs_data:
    if j['status'] == 'error':
        print(f"  - {j['name']} ({j['id'][:8]}): {j['error'][:100]}")

# Jobs in last 24h
print("\nJobs run in last 24h (Jul 13-14):")
for j in sorted(jobs_24h, key=lambda x: x['last_run']):
    print(f"  {j['last_run'][:19]} - {j['name']}: {j['status']}")

# Stuck/Model drift
stuck = [j for j in jobs_data if 'idle for' in (j['error'] or '') or 'drift' in (j['error'] or '')]
print(f"\nStuck/Model drift jobs: {len(stuck)}")
for j in stuck:
    print(f"  - {j['name']}: {j['error'][:100]}")

# Jobs with last run before July 1
old_runs = []
for j in jobs_data:
    if j['last_run']:
        try:
            run_time = datetime.fromisoformat(j['last_run'].replace('Z', '+00:00'))
            if run_time < datetime(2026, 7, 1):
                old_runs.append(j)
        except:
            pass

print(f"\nJobs with last run before July 1: {len(old_runs)}")
for j in old_runs:
    print(f"  - {j['name']}: {j['last_run'][:10]}")

# Overall success rate
overall_rate = ok_jobs / active_jobs * 100 if active_jobs > 0 else 0
print(f"\nOverall success rate (active jobs): {ok_jobs}/{active_jobs} = {overall_rate:.0f}%")

# Paused jobs (disabled)
# From cron list, all show [active] but some are disabled in jobs.json
# Check jobs.json for disabled state
print("\n--- Checking jobs.json for disabled/paused ---")
jobs_path = Path(r"C:\Users\User\.hermes\cron\jobs.json")
with open(jobs_path, 'r') as f:
    data = json.load(f)

disabled = []
for job in data.get('jobs', []):
    if not job.get('enabled', True):
        disabled.append(job)
    if job.get('state') == 'paused':
        disabled.append(job)

print(f"Disabled/Paused jobs: {len(disabled)}")
for j in disabled:
    print(f"  - {j['name']} ({j['id'][:8]}): enabled={j.get('enabled')}, state={j.get('state')}, paused_reason={j.get('paused_reason')}")