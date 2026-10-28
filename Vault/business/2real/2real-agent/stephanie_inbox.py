#!/usr/bin/env python3
"""Stephanie silent-inbox → Mum health masters processor (25/10/26).

Reads the silent-intake inbox that the whatsapp-customer-gate writes for
Stephanie (nurse, 0548236698) and PREPARES it for logging. The actual
intelligence (parsing BP/meals/meds and writing the right master entry)
is done by the agent via the elder-health-daily-logging skill — this script
standardizes the intake for it.

Usage:
  python stephanie_inbox.py read          # print new unprocessed entries
  python stephanie_inbox.py tail          # last 10 entries
  python stephanie_inbox.py mark <ts>     # mark entries up to <ts> as processed (append [PROCESSED])
"""
import sys, os, re, json, datetime

INBOX = r'C:\Users\User\.hermes\workspace\Vault\family\mum\health\STEPHANIE_INBOX.md'
STATE = r'C:\Users\User\AppData\Local\hermes\profiles\sat-nav\cache\scratch\stephanie_inbox_state.json'


def read_entries():
    if not os.path.exists(INBOX):
        return []
    t = open(INBOX, encoding='utf-8').read()
    # entries look like: ## YYYY-MM-DD HH:MM (from 233548236698)\n- <text>
    entries = []
    for m in re.finditer(r'^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \(from ([^)]+)\)\n- (.*)$', t, re.M):
        entries.append({'ts': m.group(1), 'from': m.group(2), 'text': m.group(3).strip(),
                        'processed': False})
    return entries


def load_state():
    try:
        if os.path.exists(STATE):
            return json.load(open(STATE, encoding='utf-8'))
    except Exception:
        pass
    return {'processed_ts': []}


def save_state(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(st, open(STATE, 'w', encoding='utf-8'), indent=2)


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else 'read'
    entries = read_entries()
    st = load_state()
    done = set(st.get('processed_ts', []))
    if action == 'read':
        new = [e for e in entries if e['ts'] not in done]
        print(f"{len(new)} new (unprocessed) Stephanie entries:")
        for e in new:
            print(f"\n— {e['ts']} —\n  {e['text'][:500]}")
        if not new:
            print("(none)")
    elif action == 'tail':
        for e in entries[-10:]:
            flag = ' [seen]' if e['ts'] in done else ''
            print(f"{e['ts']}{flag}: {e['text'][:120]}")
    elif action == 'mark-all':
        for e in entries:
            done.add(e['ts'])
        st['processed_ts'] = sorted(done)
        save_state(st)
        print(f"marked {len(entries)} entries as seen/processed")


if __name__ == '__main__':
    main()