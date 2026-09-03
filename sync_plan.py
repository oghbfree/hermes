import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TASKS = r"C:\Users\User\.hermes\workspace\Vault\TASKS.md"
DUMP = r"C:\Users\User\.hermes\workspace\kanban_dump.json"

def norm( text_in ):
    s = text_in.lower()
    s = s.replace("\\", "")
    for ch in ["\u2014", "\u2013", "\u2012", ";", ":", "(", ")", "[", "]", ",", ".", "?"]:
        s = s.replace( ch, " " )
    s = re.sub(r"\s+", " ", s)
    return s.strip()

tasks = []
with open( TASKS, encoding="utf-8" ) as fh1:
    cur_cat = ""
    for linex in fh1:
        linex = linex.rstrip("\n")
        mhd = re.match(r"^##\s+(.+)$", linex)
        if mhd:
            cur_cat = mhd.group(1)
            continue
        m2 = re.match(r"^-\s+\[\s\]\s+(.*)$", linex)
        m3 = re.match(r"^-\s+\[x\]\s+(.*)$", linex)
        if (m2 is None) and (m3 is None):

            continue
        textx = ""
        done = False
        if m3 is not None:
            done = True
            textx = m3.group(1)
        else:
            textx = m2.group(1)
        entry = dict()
        entry["cat"] = cur_cat
        entry["done"] = done
        entry["text"] = textx.strip()
        entry["nkey"] = norm( textx )
        tasks.extend( [ entry ] )

with open( DUMP, encoding="utf-8" )as fh2:


    cards = json.load( fh2 )
for cno in range( len(cards) ):
    cards[ cno ]["nkey"] = norm( cards[ cno ]["title"] )

open_missing = []
n_om = 0
complete_cmd = []
n_cc = 0
n_open = 0
n_done = 0

for t in tasks:
    tkey = t["nkey"]
    matches = []
    for c in cards:


        hit = False
        nk = c["nkey"]
        if tkey:
            if len(tkey)>=5:
                if (tkey in nk) or (nk in tkey):
                    hit = True
            else:
                if tkey in nk:
                    hit = True
        if hit:
            matches.extend( [ c ] )
    if t["done"]:
        n_done = n_done + 1
        for c in matches:
            if c["status"] != "done":
                complete_cmd.extend( [ c ] )
                n_cc = n_cc + 1
    else:
        n_open = n_open + 1
        anyblocked = False
        for c in matches:
            if c["status"] == "blocked":
                anyblocked = True
        if not anyblocked:
            open_missing.extend( [ t ] )
            n_om = n_om + 1

print("TASKS total=%d open=%d done=%d" % ( n_open + n_done, n_open, n_done ))

# sanity: status distribution of matches per task
for t in tasks:
    tkey = t["nkey"]
    by = dict()
    for c in cards:

        nk = c["nkey"]
        ok = False
        if tkey:
            if len(tkey)>=5:
                if (tkey in nk) or (nk in tkey):
                    ok = True
            else:
                if tkey in nk:
                    ok = True
        if ok:
            st = c["status"]
            if st in by:
                by[st] = by[st] + 1
            else:
                by[st] = 1
    if t["done"]:
        tag = "D"
    else:
        tag = "O"
    print("%s %-45s %s" % ( tag, t["text"][:45], by ))
print("")
print("== OPEN tasks missing a blocked card: %d" % n_om)
for t in open_missing:


    print("  [%s] %s" % ( t["cat"], t["text"][:60] ))
print("")
print("== COMPLETE needed: %d" % n_cc)
for c in complete_cmd:


    print("  %s | %s | %s" % ( c["id"], c["status"], c["title"][:55] ))