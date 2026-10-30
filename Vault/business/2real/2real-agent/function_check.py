#!/usr/bin/env python3
"""function_check.py — 2Real FUNCTION-TO-PRODUCT check (28/10/26, H).

Customer asks "do you have <product> that can <function>" (or hands a list of
items). This checks the REAL catalog (jiji_listings_full.json = source of truth,
NOT Zobaze) and returns what 2Real actually has that does the job.

Uses the CHEAP tier (local Ollama) to interpret the ask -> product keywords +
function/use-case, then matches the catalog on title+category+details. Returns
ranked matches with live price + an honest verdict line (have-it / maybe / don't-have).

USAGE:
  python function_check.py "silicone that works underwater"
  python function_check.py "customer wants: silicone for underwater use; also needs gorilla tape; a drill"
  python function_check.py --list "<multi-line list of items>"
  python function_check.py --match-only "silicone sealant"   # skip LLM, pure keyword match
"""
import sys, os, json, re, urllib.request

BASE = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent'
CATALOG = os.path.join(BASE, 'jiji_listings_full.json')
OLLAMA = 'http://localhost:11434'
OLLAMA_MODEL = 'gemma4:latest'
CTA = '0204252252'


def load_catalog():
    d = json.load(open(CATALOG, encoding='utf-8'))
    return d.get('items', []) if isinstance(d, dict) else d


def _ollama(prompt):
    body = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt,
                       "stream": False, "options": {"temperature": 0.2}}).encode()
    req = urllib.request.Request(OLLAMA + '/api/generate', data=body,
                                 headers={'Content-Type': 'application/json'})
    d = json.loads(urllib.request.urlopen(req, timeout=120).read())
    return (d.get('response') or '').strip()


def interpret(ask):
    """Cheap-tier: extract product keywords + function from a customer ask."""
    p = ("You help a seller match a customer request to products in stock. "
         "From the request, list the PRODUCT KEYWORDS (the thing they want, e.g. "
         "silicone, drill, tape, glue) and the FUNCTION/USE (e.g. works underwater, "
         "for wood, high temp). Reply as two lines:\n"
         "KEYWORDS: <comma list>\nFUNCTION: <short phrase>\n\nRequest: " + ask)
    raw = _ollama(p)
    kw = re.search(r'KEYWORDS:\s*(.+)', raw, re.I)
    fn = re.search(r'FUNCTION:\s*(.+)', raw, re.I)
    return {
        'keywords': [k.strip().lower() for k in (kw.group(1) if kw else ask).split(',') if k.strip()],
        'function': (fn.group(1).strip() if fn else ''),
    }


def match(keywords, items):
    """Score catalog items against keywords (title/category/details)."""
    scored = []
    kws = [k for k in keywords if k]
    for it in items:
        title = (it.get('title') or '').lower()
        cat = (it.get('category_name') or '').lower()
        det = (it.get('details') or '').lower()
        hay = title + ' ' + cat + ' ' + det
        score = 0
        for k in kws:
            if k in title: score += 3
            elif k in cat: score += 2
            elif k in det: score += 1
        if score > 0:
            scored.append((score, it))
    scored.sort(key=lambda x: -x[0])
    return scored


def verdict_line(matches, function):
    if not matches:
        return f"❌ Nothing in the current catalog matches. Could source from UK/China — ask H."
    top = matches[0][1]
    return (f"✅ Have it: {top.get('title')} — {top.get('price_title') or top.get('price_obj')} "
            f"({top.get('category_name')}). {len(matches)} possible match(es).")


def run(ask):
    items = load_catalog()
    print(f"🔍 CHECK: {ask}\n")
    interp = interpret(ask)
    kws = interp['keywords'] or [ask.strip().lower()]
    print(f"   interpreted keywords: {kws}")
    if interp['function']:
        print(f"   function/use: {interp['function']}")
    matches = match(kws, items)
    print(f"\n{verdict_line(matches, interp['function'])}\n")
    for score, it in matches[:8]:
        print(f"   [{score}] {it.get('title')[:64]} | {it.get('price_title') or it.get('price_obj')} | {it.get('category_name')}")
    print(f"\nCTA {CTA} — confirm stock before quoting (catalog may drift).")


def run_match_only(ask):
    items = load_catalog()
    kws = [k.strip().lower() for k in ask.split(',') if k.strip()]
    matches = match(kws, items)
    print(f"🔍 MATCH-ONLY: {kws} -> {len(matches)} hit(s)")
    for score, it in matches[:8]:
        print(f"   [{score}] {it.get('title')[:64]} | {it.get('price_title') or it.get('price_obj')} | {it.get('category_name')}")


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(0)
    if a[0] == '--match-only' and len(a) > 1:
        run_match_only(' '.join(a[1:])); sys.exit(0)
    if a[0] == '--list' and len(a) > 1:
        for line in ' '.join(a[1:]).splitlines():
            if line.strip(): run(line.strip()); print()
        sys.exit(0)
    run(' '.join(a))