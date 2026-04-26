import json
import os
import sys
from datetime import datetime, timezone

def main():
    json_path = r"C:\Users\User\.openclaw\cron\jobs.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    one_day_ms = 24 * 3600 * 1000
    cutoff = now_ms - one_day_ms
    
    has_fail_or_missed = False
    total = 0
    enabled = 0
    ok = 0
    fail = 0
    missed = 0
    
    lines = []
    for job in data['jobs']:
        total += 1
        if job.get('enabled', False):
            enabled += 1
        name = job.get('name', 'unnamed')
        enabled_flag = job.get('enabled', False)
        state = job.get('state', {})
        last_run_ms = state.get('lastRunAtMs')
        last_run_status = state.get('lastRunStatus')
        consecutive_errors = state.get('consecutiveErrors', 0)
        next_run_ms = state.get('nextRunAtMs')
        last_error = state.get('lastError', '')
        schedule = job.get('schedule', {})
        scheduled = schedule.get('expr', 'N/A') if schedule.get('kind') == 'cron' else 'N/A'
        
        # Determine status
        status = 'UNKNOWN'
        emoji = '�s���?'
        if last_run_status == 'ok':
            status = 'OK'
            emoji = '✅'
            ok += 1
        elif last_run_status == 'error':
            status = 'FAIL'
            emoji = '❌'
            fail += 1
        
        # Check missed
        if next_run_ms and next_run_ms < now_ms and last_run_ms and last_run_ms < next_run_ms:
            status = 'MISSED'
            emoji = '⏰'
            missed += 1
        
        if status in ('FAIL', 'MISSED'):
            has_fail_or_missed = True
        
        # Build notes
        notes = ''
        if last_error:
            notes = last_error
        if consecutive_errors > 0:
            notes += f' (Consecutive errors: {consecutive_errors})'
        if not enabled_flag:
            notes += ' [DISABLED]'
        notes = notes.strip()
        
        lines.append({
            'name': name,
            'scheduled': scheduled,
            'status': f'{emoji} {status}',
            'notes': notes
        })
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    report = f"# 🦅 DAILY CRON STATUS REPORT | {date_str}\n\n"
    report += f"**Summary:** Total: {total} | Enabled: {enabled} | ✅ OK: {ok} | ❌ FAIL: {fail} | ⏰ MISSED: {missed}\n\n"
    if has_fail_or_missed:
        report = "🚨 **ATTENTION REQUIRED: SYSTEM FRICTION DETECTED**\n\n" + report
    
    report += "| Cron Name | Scheduled | Status | Notes |\n"
    report += "| :--- | :--- | :--- | :--- |\n"
    for line in lines:
        report += f"| {line['name']} | {line['scheduled']} | {line['status']} | {line['notes']} |\n"
    
    sys.stdout.write(report)

if __name__ == '__main__':
    main()
