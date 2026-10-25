#!/usr/bin/env python3
"""Buyer-Registry Scanner + Confirm Flow (23/10/26)
Reads the WhatsApp Business chat list (via the :9222 persistent Chrome),
flags CANDIDATE repeat/B2B buyers for H to approve, then logs approved
ones to BUYER_REGISTRY.md.

Flow: scan chat list -> cross-check names/numbers against registry ->
      present candidates (name/number/last msg) -> H approves -> append.

Usage:
  python buyer_registry_scanner.py scan            # list candidate chats (no writes)
  python buyer_registry_scanner.py confirm         # interactive: Y/N per candidate, appends approved
  python buyer_registry_scanner.py approve <n>     # approve candidate #n (from last scan)
  python buyer_registry_scanner.py approve-all     # approve all candidates (from last scan)
  python buyer_registry_scanner.py status          # summary of registry + how many have numbers

Output state: cache/scratch/buyer_candidates.json
"""
import os, sys, time, json, re, datetime

sys.path.insert(0, r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent')
os.environ['FB_CDP_URL'] = 'http://127.0.0.1:9222'

VAULT = r'C:\Users\User\.hermes\workspace\Vault\business\2real'
REGISTRY = os.path.join(VAULT, 'BUYER_REGISTRY.md')
CACHE = r'C:\Users\User\AppData\Local\hermes\profiles\sat-nav\cache\scratch\buyer_candidates.json'

# Known internal/owner/team chats to never flag
KNOWN = {'2 real sales', '2real', 'sales', 'team', 'oyarifa', 'dome',
         'ethel eric room', 'group', 'broadcast', 'status', 'mum', 'mom',
         'wife', 'john', 'kyei', 'godwin', 'eben', 'sammy', 'frederick',
         'eastwood', 'ben', 'stephanie', 'senyo shop next door dome',
         '2 real sales | monday', 'private nurse', 'care'}


def get_chat_list():
    """Return [{name, number, last, unread}] from the WA Web chat list."""
    import cdp_harness as C
    C.connect(substr='web.whatsapp.com', exclude_substr=None)
    time.sleep(2)
    rows = C.js('''(() => {
      const list = document.querySelector('[data-testid="chat-list"]');
      if(!list) return [];
      const out=[];
      for(const r of list.querySelectorAll('[data-testid="cell-frame-container"]')){
        const txt=(r.innerText||'').replace(/\\n/g,' | ').trim();
        out.push(txt.slice(0,160));
      }
      return out;
    })()''')
    chats = []
    for row in (rows or []):
        # WA Web row: [<n> unread message |] <name> | <time-or-day> | <last message>
        m = re.match(r'^(?:(\d+) unread message \| )?(.*?) \| ((?:\d{1,2}:\d{2})|Yesterday|Today|[A-Z][a-z]{2}) \| (.*)$', row)
        unread = '0'
        if m:
            unread, name, _t, last = m.groups()
            name = name.strip()
        else:
            name, last = row, ''
        num = None
        nm = re.search(r'(\+?\d[\d .\-]{7,}\d)', name)
        if nm:
            num = re.sub(r'[\s.\-]', '', nm.group(1))
        if num and re.fullmatch(r'\+?\d{7,15}', name.replace(' ', '').replace('-', '').replace('.', '')):
            name = '(number)'
        chats.append({'name': name, 'number': num, 'last': last, 'unread': unread})
    return chats


def registry_numbers_and_names():
    """Return (set of numbers, set of names) already in the registry."""
    nums, names = set(), set()
    if os.path.exists(REGISTRY):
        for line in open(REGISTRY, encoding='utf-8'):
            m = re.match(r'^\|\s*\*?\*?([A-Za-z][A-Za-z .\'\-]{1,40})\*?\*?\s*\|', line)
            if m:
                names.add(m.group(1).strip().lower())
            nm = re.search(r'\|?\s*(\+?\d{9,15})\s*\|', line)
            if nm:
                nums.add(nm.group(1))
    return nums, names


def is_candidate(chat, known_nums, known_names):
    """A real person chat (not group/known/already-registered), ideally with a number."""
    n = (chat['name'] or '').lower().strip()
    if n in KNOWN:
        return False
    if chat['number'] and chat['number'] in known_nums:
        return False  # already logged
    if n in known_names:
        return False  # already logged by name
    if 'group' in n or 'room' in n or '|' in n:
        return False
    # job-applicant / non-buyer signals in the last message
    last = (chat['last'] or '').lower()
    if 'interested in the private nurse' in last or 'care position' in last or 'job' in last:
        return False
    if chat['number']:
        return True
    words = n.split()
    return len(words) >= 2 and not any(ch.isdigit() for ch in n)


def _append_to_registry(c):
    name = (c['name'] or '').strip() or '(number)'
    num = (c['number'] or '')
    last = (c['last'] or '').replace('|', ' / ')[:50]
    row = f"| {name} | {num or '❓'} | (scanned {datetime.date.today():%d/%m/%y}) {last} | ❓ |\n"
    with open(REGISTRY, 'a', encoding='utf-8') as f:
        f.write(row)


def scan():
    chats = get_chat_list()
    known_nums, known_names = registry_numbers_and_names()
    cands = []
    for c in chats:
        if is_candidate(c, known_nums, known_names):
            cands.append(c)
    with open(CACHE, 'w', encoding='utf-8') as f:
        json.dump(cands, f, ensure_ascii=False, indent=2)
    return chats, cands


def print_candidates(cands):
    print(f"\n{len(cands)} candidate repeat/B2B buyers:\n")
    for i, c in enumerate(cands, 1):
        print(f"  {i}. {c['name'] or '(number)'}  {c['number'] or '(no num)'}  | {c['last'][:45]}")


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else 'scan'
    if action == 'scan':
        chats, cands = scan()
        print(f"Scanned {len(chats)} chats. {len(cands)} NEW candidates (deduped vs registry).")
        print_candidates(cands)
        print("\nNext: buyer_registry_scanner.py confirm  (Y/N per candidate)")
    elif action == 'confirm':
        chats, cands = scan()
        print_candidates(cands)
        if not cands:
            print("No new candidates. Registry is up to date.")
            return
        print("\nApprove each? (y/n, Enter=skip, 'a'=all, 'q'=quit)")
        approved = 0
        for i, c in enumerate(cands, 1):
            label = f"{c['name'] or '(number)'} {c['number'] or ''}"
            ans = input(f"  Save {label}? [y/n/a/q] ").strip().lower()
            if ans == 'q':
                break
            if ans == 'a':
                for cc in cands[i-1:]:
                    _append_to_registry(cc)
                approved += len(cands[i-1:])
                break
            if ans == 'y':
                _append_to_registry(c)
                approved += 1
        print(f"\nDone. Logged {approved} buyer(s) to registry.")
    elif action == 'approve':
        idx = int(sys.argv[2]) - 1
        cands = json.load(open(CACHE, encoding='utf-8'))
        c = cands[idx]
        _append_to_registry(c)
        print(f"Logged: {c['name'] or c['number']} {c['number'] or ''}")
    elif action == 'approve-all':
        cands = json.load(open(CACHE, encoding='utf-8'))
        for c in cands:
            _append_to_registry(c)
        print(f"Logged {len(cands)} candidates to registry.")
    elif action == 'status':
        nums, names = registry_numbers_and_names()
        print(f"Registry: {len(names)} named buyers, {len(nums)} with phone numbers.")
        print("(Buyers with numbers = broadcast-ready. Fill the rest via '2REAL: save buyer <Name> <num>'.)")
    else:
        print(__doc__)


if __name__ == '__main__':
    main()