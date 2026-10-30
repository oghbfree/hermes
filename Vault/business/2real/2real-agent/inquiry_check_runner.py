#!/usr/bin/env python3
"""inquiry_check_runner.py — cron runner for the 2Real function-to-product check.

Reads a pending-inquiries file (CUSTOMER_INQUIRIES.md) where H pastes customer
asks, runs function_check.py on each NEW (unprocessed) line, and prints the
results for the cron to deliver. Marks processed lines so it doesn't re-run.

File format (append one ask per line, or a "LIST:" block):
  CUSTOMER: silicone that works underwater
  LIST: silicone sealant
        gorilla tape
        cordless drill

USAGE:
  python inquiry_check_runner.py            # process new inquiries, print results
  python inquiry_check_runner.py --all      # re-process everything (ignore seen)
"""
import os, sys, subprocess, datetime, re

BASE = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent'
INQ = os.path.join(BASE, 'CUSTOMER_INQUIRIES.md')
PY = r'C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe'
FC = os.path.join(BASE, 'function_check.py')
SEEN_MARK = '✅ DONE'


def read_inquiries():
    if not os.path.exists(INQ):
        return []
    lines = []
    for raw in open(INQ, encoding='utf-8'):
        l = raw.rstrip('\n')
        if not l.strip() or l.strip().startswith('#') or l.strip().startswith('|') or l.strip().startswith('>'):
            continue
        lines.append(l)
    return lines


def run_check(ask):
    p = subprocess.run([PY, FC, ask], capture_output=True, text=True, timeout=200)
    return p.stdout or p.stderr


def main():
    all_flag = '--all' in sys.argv
    lines = read_inquiries()
    new = [l for l in lines if SEEN_MARK not in l] if not all_flag else lines
    if not new:
        print("No new customer inquiries to check. (Add them to CUSTOMER_INQUIRIES.md)")
        return 0
    print(f"Checking {len(new)} inquiry line(s)...\n")
    for ask in new:
        print("=" * 60)
        print("ASK:", ask)
        print("=" * 60)
        try:
            print(run_check(ask))
        except Exception as e:
            print(f"  [error checking '{ask}']: {e}")
    # mark processed (append a DONE marker underneath each processed line)
    if not all_flag:
        content = open(INQ, encoding='utf-8').read()
        for ask in new:
            # only mark if not already marked (idempotent)
            content = content.replace(ask + '\n', ask + f'  {SEEN_MARK}\n', 1)
        open(INQ, 'w', encoding='utf-8').write(content)
        print(f"\nMarked {len(new)} line(s) as processed in {INQ}")
    return 0


if __name__ == '__main__':
    sys.exit(main())