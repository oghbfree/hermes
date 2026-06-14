import re, subprocess, sys, json, pathlib

TASKS = pathlib.Path(r'C:/Users/User/.hermes/workspace/TASKS.md')
text = TASKS.read_text(encoding='utf-8')

tasks = []
current_category = None
for line in text.splitlines():
    m = re.match(r'^##\s+(.+)$', line)
    if m:
        current_category = m.group(1).strip()
        continue
    tm = re.match(r'^- \[( |x)\]\s+(.+)$', line)
    if tm:
        tasks.append({'status': 'pending' if tm.group(1) == ' ' else 'done', 'title': tm.group(2).strip(), 'category': current_category})

kanban_res = subprocess.run(['hermes', 'kanban', 'list'], capture_output=True, text=True)
board_text = kanban_res.stdout
print('BOARD:')
print(board_text)
cards = []  # list of dicts
card_re = re.compile(r'^([✓⊘▶])\s+(t_\w+)\s+(\S+)\s+\(([^)]+)\)\s+(.*)$')
for line in board_text.splitlines():
    m = card_re.match(line)
    if m:
        symbol, cid, status, assignee, title = m.groups()
        cards.append({'symbol': symbol, 'id': cid, 'status': status, 'assignee': assignee, 'title': title.strip()})
print('CARDS:', len(cards))
for c in cards:
    print(c)
print('TASKS:', len(tasks))
for t in tasks:
    print(t)
