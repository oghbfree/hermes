#!/usr/bin/env python3
"""DECISION LOG — item 5 (27/10/26). Log every approved/reversed decision so the
stack hardens. Append a decision to the shared decision log + it becomes a candidate
for skill auto-append.

USAGE:
  python decision_log.py log "<decision text>" --tags approved,sales
  python decision_log.py recent [n]
  python decision_log.py --auto-suggest   # print decisions not yet in any skill
"""
import sys, os, re, json, datetime

DECISION_LOG = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\DECISION_LOG.md'
APPENDED_STATE = r'C:\Users\User\AppData\Local\hermes\profiles\sat-nav\cache\scratch\decision_appended.json'


def now_ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def log_decision(text, tags=None):
    tags = tags or []
    tag_str = ' '.join(f'`#{t}`' for t in tags)
    entry = f"- **{now_ts()}** {text} {tag_str}\n"
    with open(DECISION_LOG, 'a', encoding='utf-8') as f:
        f.write(entry)
    print(f"logged: {text[:60]}…")
    return entry


def recent(n=8):
    if not os.path.exists(DECISION_LOG):
        return []
    lines = [l for l in open(DECISION_LOG, encoding='utf-8') if l.strip().startswith('- **')]
    return lines[-n:]


def main():
    a = sys.argv[1:]
    if a and a[0] == 'log' and len(a) > 1:
        tags = []
        # parse --tags tag1,tag2
        for i, x in enumerate(a):
            if x == '--tags' and i + 1 < len(a):
                tags = a[i + 1].split(',')
        text = ' '.join([x for x in a[1:] if not x.startswith('--')])
        log_decision(text, tags)
    elif a and a[0] == 'recent':
        print('\n'.join(recent(int(a[1]) if len(a) > 1 else 8)))
    elif a and a[0] == '--auto-suggest':
        print("No auto-suggest wiring yet — decisions are candidates for skill append (see HOUSE_RULES item 5).")
    else:
        print("usage: decision_log.py log <text> [--tags a,b] | recent [n]")


if __name__ == '__main__':
    main()