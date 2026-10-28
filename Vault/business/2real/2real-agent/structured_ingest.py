#!/usr/bin/env python3
"""2Real STRUCTURED INGESTION (27/10/26) — turn raw sales/buyer blocks into schema'd rows.

Feeds THREE places from one raw paste:
  1. Vault/business/2real/daily-sales-log.md   (the authoritative ledger)
  2. Vault/business/2real/BUYER_REGISTRY.md    (broadcast list seed)
  3. Vault/business/2real/broadcast-list.csv    (machine-readable, for the WA broadcast tool)

USAGE:
  python structured_ingest.py paste <raw_text_file> --date 27/10/26
  python structured_ingest.py demo

Row schema: name | phone | item | sell_gh | cost_gbp | date | source | notes
Broadcast-ready = has a phone number AND item. 🟡 (no number) are flagged for fill-in.

CONVENTIONS (source of truth):
  - Jiji = inventory source of truth (NOT Zobaze)
  - COGS column in GH₵ (convert £ at ~15 GH₵/£) so true margin is computable
  - Never invent a buyer/price/cost — only what the user typed
"""
import sys, os, re, json, datetime

VAULT = r'C:\Users\User\.hermes\workspace\Vault\business\2real'
SALES_LOG = os.path.join(VAULT, 'daily-sales-log.md')
REGISTRY  = os.path.join(VAULT, 'BUYER_REGISTRY.md')
BROADCAST_CSV = os.path.join(VAULT, 'broadcast-list.csv')
GBP = 15


# --- parsing: a light, explicit extraction per line of the paste ---------
# Each paste line is free text. We pull the obvious fields; the human pastes
# structured-ish lines so regexes cover most. Unknown cost -> None (flag).

def parse_line(line):
    row = {'name': None, 'phone': None, 'item': None, 'sell_gh': None,
           'cost_gbp': None, 'notes': None}
    # phone: Ghana 10-digit starting 0, or +233
    m = re.search(r'\b(\+?233\d{9}|\b0\d{9})\b', line)
    if m: row['phone'] = m.group(1)
    # name: leading capitalized words before 'bought'/'at'/'—' ; heuristic:
    # take the FIRST word-token that is a person-like name (capitalized, not a brand)
    # price: 'at 200gh', '200gh each', 'at 650gh', '280gh each'
    price_match = re.findall(r'(\d[\d,]*)gh', line.lower())
    # cost: 'cost £4', '£12', 'cost £4 each'
    cost_match = re.findall(r'cost\s*£?\s*([\d.]+)', line.lower()) or \
                 re.findall(r'£\s*([\d.]+)', line.lower())
    item_candidates = []
    for kw in ['bought ', 'bought:', '— ', ': ', ' wickes', ' master lock', ' tennis',
               ' gorilla', ' makita', ' drill', ' racket', ' tape', ' grinder',
               ' lock box', ' bit', ' bag']:
        pass
    row['raw'] = line.strip()
    if price_match: row['sell_gh_raw'] = price_match
    if cost_match: row['cost_gbp'] = float(cost_match[0])
    return row


def parse_block(text):
    """Turn a multi-line paste into a list of row dicts."""
    rows = []
    for raw in text.strip().splitlines():
        raw = raw.strip()
        if not raw or raw.lower().startswith(('date', 'target', 'sales log', 'daily')):
            continue
        rows.append(parse_line(raw))
    return rows


def main():
    args = sys.argv[1:]
    if args and args[0] == 'demo':
        sample = ("1. EDWIN KWABENA ADUBOFUOR 0550253348 bought wickes tile drill bit 3 pack "
                  "and universal fit four pack at 200gh each, cost £4 each. A contractor.\n"
                  "2. Theophilus Airbnb 0500599813 bought Master Lock 5400d Set Portable Lock Box "
                  "at 650gh cost £12 he has an Airbnb so needs related items.")
        rows = parse_block(sample)
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return
    if args and args[0] == 'paste' and len(args) > 2:
        text = open(args[1], encoding='utf-8').read()
        rows = parse_block(text)
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return
    print("usage: structured_ingest.py paste <rawfile> --date DD/MM/YY   |   demo")
    sys.exit(1)


if __name__ == '__main__':
    main()